import sqlite3
import os
import sys
import re
import json
import zipfile
from datetime import datetime
from pypdf import PdfReader

APPDATA = os.environ.get('APPDATA', '')
NET2_DIR = os.path.join(APPDATA, 'net2offlineclient')
DOCS_DIR = os.path.join(NET2_DIR, 'documents')
SCRIPTS_DIR = os.path.join(NET2_DIR, 'scripts')

# Local save paths for exam questions and verified answers
WORKSPACE_DIR = os.environ.get('NETAPP_RAG_DIR', os.path.dirname(os.path.abspath(__file__)))
HISTORY_MD = os.path.join(WORKSPACE_DIR, 'historico_questoes.md')
HISTORY_JSON = os.path.join(WORKSPACE_DIR, 'historico_questoes.json')

def get_toc_map():
    toc_path = os.path.join(NET2_DIR, 'toc.sqlite')
    if not os.path.exists(toc_path):
        return {}
    conn = sqlite3.connect(toc_path)
    conn.row_factory = sqlite3.Row
    tocs = {row['TocId']: dict(row) for row in conn.execute("SELECT * FROM TableOfContent").fetchall()}
    conn.close()
    return tocs

def get_groups_map():
    db_path = os.path.join(NET2_DIR, 'net2offlineclient.sqlite')
    if not os.path.exists(db_path):
        return {}
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    groups = {row['Id']: row['Name'] for row in conn.execute("SELECT Id, Name FROM UserGroups").fetchall()}
    conn.close()
    return groups

TOCS = get_toc_map()
GROUPS = get_groups_map()

def build_breadcrumb(toc_id, group_id=None):
    path = []
    curr = toc_id
    visited = set()
    while curr is not None and curr in TOCS and curr not in visited:
        visited.add(curr)
        name = TOCS[curr]['TocName']
        if name:
            path.append(name.strip())
        curr = TOCS[curr]['ParentTocId']
    path.reverse()
    
    group_name = GROUPS.get(group_id, '')
    parts = ["Net2"]
    if group_name and (not path or path[0] != group_name):
        parts.append(group_name)
    parts.extend(path)
    return " > ".join(parts)

def search_catalog(query, limit=15):
    docs_path = os.path.join(NET2_DIR, 'documents.sqlite')
    if not os.path.exists(docs_path):
        return []
    conn = sqlite3.connect(docs_path)
    conn.row_factory = sqlite3.Row
    tokens = [t.strip() for t in query.split() if t.strip()]
    if not tokens:
        return []
    
    where_clauses = []
    params = []
    for t in tokens:
        where_clauses.append("(DocumentName LIKE ? OR FilePath LIKE ? OR Description LIKE ? OR Keywords LIKE ?)")
        param = f"%{t}%"
        params.extend([param, param, param, param])
    
    sql = f"SELECT DocumentId, DocumentName, TocId, GroupId, GroupName, FilePath, Downloaded FROM Documents WHERE {' AND '.join(where_clauses)} LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            'DocumentId': r['DocumentId'],
            'DocumentName': r['DocumentName'],
            'FilePath': r['FilePath'],
            'Downloaded': r['Downloaded'],
            'Breadcrumb': build_breadcrumb(r['TocId'], r['GroupId'])
        })
    return results

def search_in_pdf(pdf_filename, query_regex, max_snippets=3):
    clean_name = os.path.basename(pdf_filename)
    full_path = os.path.join(DOCS_DIR, clean_name)
    if not os.path.exists(full_path):
        return []
    
    snippets = []
    try:
        reader = PdfReader(full_path)
        pattern = re.compile(query_regex, re.IGNORECASE)
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            for match in pattern.finditer(text):
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                snippet = text[start:end].replace('\n', ' ').strip()
                snippets.append((page_idx + 1, snippet))
                if len(snippets) >= max_snippets:
                    return snippets
    except Exception as e:
        return [(-1, f"Error reading PDF: {e}")]
    return snippets

def search_in_scripts(keyword, max_matches=5):
    """Searches within Net2 Action Plan zip files in the scripts folder."""
    if not os.path.exists(SCRIPTS_DIR):
        return []
    matches = []
    kw_bytes = keyword.lower().encode('utf-8')
    for fname in os.listdir(SCRIPTS_DIR):
        if fname.endswith('.zip'):
            zpath = os.path.join(SCRIPTS_DIR, fname)
            try:
                with zipfile.ZipFile(zpath, 'r') as z:
                    for inner_file in z.namelist():
                        if inner_file.endswith(('.html', '.htm', '.json', '.txt', '.js')):
                            content = z.read(inner_file).lower()
                            if kw_bytes in content:
                                matches.append({
                                    'zip': fname,
                                    'file': inner_file
                                })
                                if len(matches) >= max_matches:
                                    return matches
            except Exception:
                continue
    return matches

def save_qa(question, options, correct_option, net2_path, rationale="", anti_trap_notes=""):
    """
    Saves question, options, highlighted answer, Net2 path, and notes to local Markdown and JSON files.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Update JSON database
    entry = {
        "timestamp": timestamp,
        "question": question,
        "options": options,
        "correct_option": correct_option,
        "net2_path": net2_path,
        "rationale": rationale,
        "anti_trap_notes": anti_trap_notes
    }
    
    history = []
    if os.path.exists(HISTORY_JSON):
        try:
            with open(HISTORY_JSON, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append(entry)
    
    with open(HISTORY_JSON, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
        
    # 2. Append to Markdown file
    q_num = len(history)
    md_content = f"\n## Questão {q_num} - {timestamp}\n\n"
    md_content += f"📋 **TRANSCRIÇÃO DA QUESTÃO (ENGLISH):**\n"
    md_content += f"> {question}\n>\n"
    for opt in options:
        opt_clean = opt.strip()
        is_correct = opt_clean.upper().startswith(correct_option.strip().upper()) or (correct_option.strip() in opt_clean)
        if is_correct:
            md_content += f"> <mark style=\"background-color: #ffeb3b; color: #000; font-weight: bold; padding: 2px 6px; border-radius: 3px;\">➔ {opt_clean}</mark>  \n"
        else:
            md_content += f"> {opt_clean}  \n"
            
    md_content += f"\n---\n\n"
    md_content += f"🎯 **RESPOSTA CORRETA:** **{correct_option}**\n\n"
    md_content += f"📍 **CAMINHO NO NET2:**\n`{net2_path}`\n\n"
    md_content += f"🔍 **DUPLA CHECAGEM & ANÁLISE DE PEGADINHA:**\n"
    if anti_trap_notes:
        md_content += f"• **Atenção ao Enunciado:** {anti_trap_notes}\n"
    if rationale:
        md_content += f"• **Evidência no Net2:** {rationale}\n"
    md_content += f"\n---\n"
    
    with open(HISTORY_MD, 'a', encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"[OK] Questão {q_num} salva com sucesso em:")
    print(f"  - {HISTORY_MD}")
    print(f"  - {HISTORY_JSON}")
    return q_num

if __name__ == '__main__':
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        print(f"Searching catalog for: {q}")
        res = search_catalog(q)
        for r in res:
            print(f"\n[DOC] {r['DocumentName']}")
            print(f"  Path: {r['Breadcrumb']}")
            print(f"  File: {r['FilePath']} (Downloaded: {r['Downloaded']})")
    else:
        print("Usage: python netapp_rag.py <query>")
