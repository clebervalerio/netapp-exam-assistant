# NetApp Exam & Net2 Assistant for Antigravity

Plugin nativo para o **Google Antigravity** que integra com a base local do **NetApp Net2 Offline Client** (`%APPDATA%\net2offlineclient`) para resolver questões de certificação e suporte (ASE-2, TPM, ONTAP, StorageGRID) com dupla checagem e zero alucinações.

---

## ⚡ Instalação Automática pelo Chat do Antigravity

Qualquer pessoa com o Antigravity instalado pode apenas colar este comando no chat:

```text
Instale e configure o plugin NetApp Exam a partir do repositório:
https://github.com/clebervalerio/netapp-exam-assistant
```

O próprio Antigravity clona o repositório, instala a dependência (`pypdf`), copia o plugin para a pasta global e valida a conexão com o Net2.

---

## 💻 Instalação Manual (Alternativa)

1. Clone o repositório:
   ```bash
   git clone https://github.com/clebervalerio/netapp-exam-assistant.git
   cd netapp-exam-assistant
   ```
2. Execute o instalador:
   ```bash
   python install.py
   ```
   *(ou dê dois cliques em `instalar_plugin_no_antigravity.bat` no Windows)*

---

## 🎯 Como Funciona

Sempre que uma questão ou print for enviado:
1. **Transcrição Fiel em Inglês** do enunciado e das alternativas.
2. **Destaque em Amarelo** da alternativa correta.
3. **Caminho Oficial no Net2** (`Net2 > Menu > Submenu > Job Aid`).
4. **Dupla Checagem & Filtro de Pegadinhas** (termos como *NOT*, *EXCEPT*, inversões de perspectiva).
5. **Registro Automático** no histórico de estudos local.
