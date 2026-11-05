import os
import sys
import shutil
import subprocess

def main():
    print("=" * 65)
    print("  INSTALADOR NATIVO - NETAPP EXAM ASSISTANT PARA ANTIGRAVITY")
    print("=" * 65)

    # 1. Instala dependência pypdf
    print("\n[1/3] Instalando dependências (pypdf)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
        print("[OK] pypdf instalado com sucesso.")
    except Exception as e:
        print(f"[AVISO] Não foi possível executar pip automaticamente: {e}")

    # 2. Localiza diretório de plugins do Antigravity
    user_home = os.path.expanduser("~")
    gemini_dir = os.path.join(user_home, ".gemini", "config", "plugins", "netapp-exam-assistant")
    print(f"\n[2/3] Instalando plugin em: {gemini_dir}")

    source_dir = os.path.dirname(os.path.abspath(__file__))
    # Se estiver rodando da raiz com subpasta netapp-exam-assistant
    plugin_source = os.path.join(source_dir, "netapp-exam-assistant")
    if not os.path.exists(plugin_source):
        plugin_source = source_dir

    os.makedirs(gemini_dir, exist_ok=True)
    
    # Copia arquivos essenciais
    for item in ["plugin.json", "rules", "skills"]:
        s = os.path.join(plugin_source, item)
        d = os.path.join(gemini_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        elif os.path.isfile(s):
            shutil.copy2(s, d)

    print("[OK] Arquivos do plugin instalados na pasta global do Antigravity.")

    # 3. Teste do Net2
    print("\n[3/3] Validando acesso ao Net2 Offline Client...")
    try:
        from skills.netapp_rag.scripts import netapp_rag
    except Exception:
        sys.path.append(os.path.join(gemini_dir, "skills", "netapp_rag", "scripts"))
        import netapp_rag
        
    appdata = os.environ.get("APPDATA", "")
    net2_dir = os.path.join(appdata, "net2offlineclient")
    if os.path.exists(net2_dir):
        print(f"[OK] Net2 Offline Client encontrado em: {net2_dir}")
        tocs = netapp_rag.get_toc_map()
        print(f"[OK] Banco de navegação: {len(tocs)} seções ativas.")
    else:
        print(f"[AVISO] Pasta do Net2 não encontrada em: {net2_dir}")

    print("\n" + "=" * 65)
    print("INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
    print("Agora você pode abrir qualquer conversa no Antigravity e mandar")
    print("as questões ou prints que ele responderá automaticamente.")
    print("=" * 65)

if __name__ == "__main__":
    main()

