#!/bin/bash

echo "========================================"
echo "  Extrator de Audio MP4 para Transcricao"
echo "========================================"
echo ""
echo "Configurado para arquivos de ate 1GB"
echo ""

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependencias se necessario
echo "Verificando dependencias..."
pip install -r requirements.txt

# Executa a aplicacao
echo ""
echo "Iniciando aplicacao..."
echo "Acesse: http://localhost:8501"
echo ""
echo "Pressione Ctrl+C para parar"
echo ""
streamlit run app.py --server.maxUploadSize=1024 --server.maxMessageSize=1024 