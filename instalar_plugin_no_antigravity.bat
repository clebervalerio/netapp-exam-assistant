@echo off
chcp 65001 >nul
echo ====================================================================
echo   INSTALADOR NATIVO DO PLUGIN NETAPP EXAM PARA O ANTIGRAVITY
echo ====================================================================
echo.

set "TARGET_DIR=%USERPROFILE%\.gemini\config\plugins\netapp-exam-assistant"
echo [1/3] Instalando dependencia Python (pypdf)...
pip install pypdf
if %errorlevel% neq 0 (
    echo [AVISO] Falha ao instalar pypdf via pip. Certifique-se de que o Python esta no PATH.
)
echo.

echo [2/3] Instalando Plugin no Antigravity...
echo Destino: %TARGET_DIR%
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"
if not exist "%TARGET_DIR%\rules" mkdir "%TARGET_DIR%\rules"
if not exist "%TARGET_DIR%\skills\netapp_rag\scripts" mkdir "%TARGET_DIR%\skills\netapp_rag\scripts"

xcopy /y /e /i "netapp-exam-assistant\*" "%TARGET_DIR%\" >nul
if %errorlevel% neq 0 (
    echo Copiando arquivos locais do plugin...
    copy /y "plugin.json" "%TARGET_DIR%\" >nul 2>&1
)

echo.
echo [3/3] Validando acesso ao Net2 Offline Client...
python verificar_ambiente.py

echo.
echo ====================================================================
echo   PLUGIN INSTALADO COM SUCESSO DENTRO DO ANTIGRAVITY!
echo ====================================================================
echo Agora o Antigravity ja possui o plugin nativo instalado.
echo Qualquer pessoa pode simplesmente abrir o Antigravity e mandar prints
echo ou textos de questoes sem precisar pedir para abrir ou carregar nada!
echo ====================================================================
pause

