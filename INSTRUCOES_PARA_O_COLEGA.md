# Como Instalar o Assistente Nativo da NetApp no Antigravity

Este pacote transforma o assistente de prova em um **Plugin Nativo do Antigravity**.

A vantagem do **Plugin Nativo**:
* **Não precisa abrir pasta específica no Antigravity.**
* **Não precisa pedir pro assistente "abrir arquivo", "carregar o programa" ou "iniciar o script".**
* O Antigravity já inicia com o conhecimento, as regras da prova e as ferramentas do Net2 carregadas nativamente na memória em qualquer conversa.

---

## Passo 1: Instalação (1 Clique)
1. Dê dois cliques no arquivo:
   `instalar_plugin_no_antigravity.bat`
2. O instalador copiará o plugin diretamente para a pasta global de plugins do Antigravity (`%USERPROFILE%\.gemini\config\plugins\netapp-exam-assistant`) e instalará a dependência do Python (`pypdf`).

---

## Passo 2: Como Usar
1. Abra o **Antigravity**.
2. Abra qualquer chat ou conversa.
3. Cole o print ou o texto de qualquer questão da prova NetApp.
4. **Pronto!** O Antigravity reconhecerá automaticamente a pergunta, fará a consulta no Net2 local, destacará a resposta certa em amarelo e colocará o caminho do Net2 logo abaixo.

---

## Dica de Velocidade
* Colar o texto da questão (usando o `Win + Shift + S` do Windows e clicando em "Copiar Texto") responde em **poucos segundos** (2 a 5s).
* Enviar o print de tela também funciona perfeitamente, levando cerca de 15 a 20s para processar a visão.
