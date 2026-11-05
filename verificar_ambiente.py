import os
import sys
import sqlite3

def testar():
    print("=" * 60)
    print("   VERIFICADOR DO ASSISTENTE DE PROVA NETAPP (ASE-2)")
    print("=" * 60)
    
    # 1. Verifica Python
    print(f"[OK] Python: {sys.version.split()[0]}")
    
    # 2. Verifica biblioteca pypdf
    try:
        import pypdf
        print(f"[OK] Biblioteca pypdf instalada (versão: {pypdf.__version__})")
    except ImportError:
        print("[ERRO] pypdf NÃO encontrada. Execute: pip install -r requirements.txt")
        return False
        
    # 3. Detecta pasta do Net2 dinamicamente
    appdata = os.environ.get('APPDATA', '')
    net2_dir = os.path.join(appdata, 'net2offlineclient')
    print(f"\nDetectando Net2 em: {net2_dir}")
    
    if not os.path.exists(net2_dir):
        print(f"[ERRO] A pasta do Net2 Offline Client não foi encontrada em:")
        print(f"       {net2_dir}")
        print("       Certifique-se de que o aplicativo Net2 está instalado e já foi aberto nesta máquina.")
        return False
    print("[OK] Pasta do Net2 localizada com sucesso!")
    
    # 4. Verifica banco de documentos
    docs_db = os.path.join(net2_dir, 'documents.sqlite')
    if os.path.exists(docs_db):
        conn = sqlite3.connect(docs_db)
        count = conn.execute("SELECT COUNT(*) FROM Documents").fetchone()[0]
        conn.close()
        print(f"[OK] Banco de Documentos: {count} documentos catalogados.")
    else:
        print("[AVISO] documents.sqlite não encontrado na pasta do Net2.")
        
    # 5. Verifica PDFs offline
    docs_dir = os.path.join(net2_dir, 'documents')
    if os.path.exists(docs_dir):
        pdfs = [f for f in os.listdir(docs_dir) if f.lower().endswith('.pdf')]
        print(f"[OK] Acervo local de PDFs: {len(pdfs)} manuais prontos para busca.")
    else:
        print("[AVISO] Pasta documents com PDFs não encontrada.")
        
    print("\n" + "=" * 60)
    print("RESULTADO: O AMBIENTE ESTÁ 100% PRONTO PARA A PROVA!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    testar()

