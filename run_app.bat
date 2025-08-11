@echo off
echo ========================================
echo   Extrator de Audio MP4 para Transcricao
echo ========================================
echo.
echo Configurado para arquivos de ate 1GB
echo.

REM Verifica se o ambiente virtual existe
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativa o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instala dependencias se necessario
echo Verificando dependencias...
pip install -r requirements.txt

REM Executa a aplicacao
echo.
echo Iniciando aplicacao...
echo Acesse: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar
echo.
streamlit run app.py --server.maxUploadSize=1024 --server.maxMessageSize=1024

pause 