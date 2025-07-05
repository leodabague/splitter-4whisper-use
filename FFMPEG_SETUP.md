# Configuração do FFmpeg

Este projeto usa as bibliotecas `pydub` e `moviepy` que dependem do FFmpeg para processar arquivos de áudio e vídeo.

## Problema

Se você ver os seguintes avisos ao executar o Streamlit:

```
RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
RuntimeWarning: Couldn't find ffprobe or avprobe - defaulting to ffprobe, but may not work
```

Isso significa que o FFmpeg não está instalado ou não está no PATH do sistema.

## Solução

### Opção 1: Usar o script automático (Recomendado)

1. Execute o PowerShell como administrador
2. Navegue até a pasta do projeto
3. Execute o script de configuração:

```powershell
.\setup-ffmpeg.ps1
```

4. Reinicie o terminal

### Opção 2: Instalação manual

1. Instale o FFmpeg via winget:
```powershell
winget install ffmpeg
```

2. Adicione manualmente ao PATH:
   - Abra as Configurações do Sistema
   - Vá para Variáveis de Ambiente
   - Adicione o caminho do FFmpeg ao PATH do usuário:
   ```
   C:\Users\[SEU_USUARIO]\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin
   ```

### Opção 3: Instalação via Chocolatey

1. Instale o Chocolatey (se não tiver):
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

2. Instale o FFmpeg:
```powershell
choco install ffmpeg -y
```

## Verificação

Para verificar se o FFmpeg está funcionando, execute:

```powershell
ffmpeg -version
ffprobe -version
```

Se ambos os comandos retornarem informações de versão, o FFmpeg está configurado corretamente.

## Executando o projeto

Após configurar o FFmpeg, execute o projeto normalmente:

```powershell
uv run streamlit run app.py
```

O aplicativo estará disponível em: http://localhost:8501 