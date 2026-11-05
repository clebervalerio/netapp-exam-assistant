@echo off
chcp 65001 >nul
echo ===================================================
echo   Configurando Assistente de Prova NetApp (ASE-2)
echo ===================================================
echo.
echo [1/2] Instalando dependencias (pypdf)...
pip install -r requirements.txt
echo.
echo [2/2] Testando conexao com o Net2 Offline Client...
python verificar_ambiente.py
echo.
pause

