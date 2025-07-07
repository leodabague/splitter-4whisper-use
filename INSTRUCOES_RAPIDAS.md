# 🚀 Instruções Rápidas - Extrator de Áudio MP4

## ✅ Configuração Completa (1GB de limite)

### 1. Execução Simples
```bash
cd splitter-4whisper-use
streamlit run app.py
```

### 2. Execução com Configuração Explícita
```bash
cd splitter-4whisper-use
streamlit run app.py --server.maxUploadSize=1024 --server.maxMessageSize=1024
```

### 3. Scripts Automáticos
- **Windows**: Execute `run_app.bat`
- **Linux/macOS**: Execute `./run_app.sh`

## 📁 Arquivos Criados

- ✅ `.streamlit/config.toml` - Configuração de 1GB
- ✅ `streamlit_config.py` - Configurações Python
- ✅ `test_config.py` - Teste de configuração
- ✅ `run_app.bat` - Script Windows
- ✅ `run_app.sh` - Script Linux/macOS

## 🎯 Resultado

- **Limite anterior**: 200MB
- **Limite atual**: **1GB (1024 MB)**
- **Melhoria**: 5x maior capacidade

## 🔧 Verificação

Para testar se tudo está funcionando:
```bash
streamlit run test_config.py
```

## 📊 Casos de Uso

| Tipo de Reunião | Duração | Tamanho Original | Tamanho Otimizado |
|-----------------|---------|------------------|-------------------|
| Reunião Curta | 30min | ~100MB | ~15MB |
| Reunião Normal | 1h | ~200MB | ~28MB |
| Reunião Longa | 2h | ~400MB | ~56MB |
| Palestra | 3h | ~600MB | ~84MB |
| Conferência | 4h | ~800MB | ~112MB |

## ⚡ Dicas

1. **Formato recomendado**: M4A 64kbps
2. **Configuração ideal**: 16kHz, Mono
3. **Para transcrição**: Qualidade suficiente, tamanho mínimo
4. **Arquivos grandes**: Use divisão automática em chunks

## 🐛 Solução de Problemas

### Erro de Upload
- Verifique se o arquivo `.streamlit/config.toml` existe
- Reinicie a aplicação
- Use linha de comando com parâmetros explícitos

### Erro do FFmpeg
- Instale FFmpeg: `winget install Gyan.FFmpeg` (Windows)
- Verifique se está no PATH
- Reinicie o terminal

### Performance
- Para arquivos muito grandes (>500MB), o processamento pode demorar
- Use a barra de progresso para acompanhar
- Considere dividir arquivos muito grandes manualmente 