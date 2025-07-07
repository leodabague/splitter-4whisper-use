# 🎵 Extrator de Áudio MP4 para Transcrição

Aplicação Streamlit para extrair e otimizar áudio de arquivos MP4 para transcrição, com suporte a arquivos de até **1GB**.
*IDEAL* para workflows de transcrição de audio de reuniões para insights, ata e acompanhamento.

## 🎯 Exemplos de Redução:
| Tipo de Reunião |	Duração | Tamanho Original | Tamanho Otimizado |
|-----------------|---------|------------------|-------------------|
| Reunião Curta | 30min | ~100MB | ~15MB |
| Reunião Normal |	1h |	~200MB |	~28MB |
| Reunião Longa |	2h |	~400MB |	~56MB |
| Palestra |	3h |	~600MB |	~84MB |
| Conferência |	4h |	~800MB |	~112MB |

## 🚀 Características

- ✅ **Limite de upload: 1GB** (configurado)
- 🎯 **Otimizado para transcrição** (menor tamanho possível)
- 📁 **Múltiplos formatos**: M4A, MP3, WEBM, MPGA, WAV
- ✂️ **Divisão automática** em chunks de 20MB
- 🔧 **Configurações otimizadas**: 16kHz, Mono, 64kbps

## 📋 Pré-requisitos

### 1. Instalar FFmpeg
```bash
# Windows (via winget)
winget install Gyan.FFmpeg

# macOS (via Homebrew)
brew install ffmpeg
```

### 2. Instalar dependências Python
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Como Executar

### Execução Normal
```bash
cd splitter-4whisper-use
streamlit run app.py --server.maxUploadSize=1024 --server.maxMessageSize=1024
```

## ⚙️ Configuração

A aplicação já está configurada para aceitar arquivos de até 1GB através do arquivo `.streamlit/config.toml`:

```toml
[server]
maxUploadSize = 1024  # 1GB em MB
maxMessageSize = 1024 # 1GB em MB
enableWebsocketCompression = true
```

## 📊 Formatos e Tamanhos

### Entrada
- **Formato**: MP4
- **Tamanho máximo**: 1GB (1024 MB)

### Saída (otimizada para transcrição)
| Formato | Bitrate | Tamanho (1h) | Recomendação |
|---------|---------|--------------|--------------|
| M4A | 64kbps | ~28MB | ⭐ Melhor |
| MP3 | 64kbps | ~28MB | ✅ Compatível |
| WEBM | 64kbps | ~25MB | 🆕 Moderno |
| WAV | 16kHz | ~115MB | 📊 Qualidade |

## 🎯 Fluxo de Trabalho

1. **Upload**: Carregue seu arquivo MP4 (até 1GB)
2. **Configuração**: Escolha formato e configurações
3. **Processamento**: Extração e otimização automática
4. **Download**: Arquivo único ou dividido em chunks

## 🔧 Configurações Técnicas

### Otimizações para Transcrição
- **Sample Rate**: 16kHz (suficiente para voz)
- **Canais**: Mono (reduz tamanho em 50%)
- **Bitrate**: 64kbps (qualidade adequada)
- **Formato**: M4A (melhor compressão)

### Divisão de Arquivos
- **Tamanho máximo por chunk**: 20MB
- **Divisão automática**: Baseada no tamanho
- **Download**: Arquivo ZIP com todos os chunks

## 🐛 Solução de Problemas

### Erro de Upload
Se receber erro de limite de upload:
1. Verifique se o arquivo `.streamlit/config.toml` existe
2. Reinicie a aplicação: `streamlit run app.py`
3. Use linha de comando com parâmetros explícitos

### Erro do FFmpeg
Se o FFmpeg não for encontrado:
1. Instale o FFmpeg conforme pré-requisitos
2. Verifique se está no PATH do sistema
3. Reinicie o terminal/IDE

## 📈 Casos de Uso

### Reuniões Longas
- **Duração**: 2-3 horas
- **Tamanho original**: 500MB-1GB
- **Resultado**: 50-100MB otimizado

### Gravações de Palestras
- **Duração**: 1-2 horas
- **Tamanho original**: 200-500MB
- **Resultado**: 25-50MB otimizado

### Entrevistas
- **Duração**: 30-60 minutos
- **Tamanho original**: 100-200MB
- **Resultado**: 15-30MB otimizado

## 🔄 Integração com Transcrição

Após extrair o áudio otimizado, você pode usar:

- **Whisper**: `whisper audio.m4a`
- **OpenAI Whisper API**: Para transcrição online
- **Google Speech-to-Text**: Para transcrição em português
- **Azure Speech Services**: Para transcrição empresarial

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para detalhes.
