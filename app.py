import streamlit as st
import os
import tempfile
from pathlib import Path
import math
import zipfile
import io
import subprocess
import warnings

# Configuração do Streamlit para aumentar limite de upload para 1GB
st.set_page_config(
    page_title="Extrator de Áudio MP4",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importa configurações personalizadas
try:
    from streamlit_config import configure_streamlit, show_upload_info
    configure_streamlit()
except ImportError:
    # Se o arquivo de configuração não existir, usa configuração básica
    pass

# Suprimir warnings do pydub sobre ffmpeg
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg")
warnings.filterwarnings("ignore", message="Couldn't find ffprobe")

# Configuração do FFmpeg ANTES de importar pydub
def setup_ffmpeg():
    """Configura o caminho do FFmpeg para o pydub"""
    import platform
    
    # Caminho do FFmpeg instalado via winget no Windows
    if platform.system() == "Windows":
        ffmpeg_path = os.path.expanduser("~/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-7.1.1-full_build/bin")
        
        if os.path.exists(ffmpeg_path):
            # Adiciona ao PATH do processo atual ANTES de importar pydub
            if ffmpeg_path not in os.environ.get('PATH', ''):
                os.environ['PATH'] = ffmpeg_path + os.pathsep + os.environ.get('PATH', '')
            
            return True
    
    return False

# Configura o FFmpeg ANTES de importar pydub
setup_ffmpeg()

# Agora importa pydub após configurar o PATH
from pydub import AudioSegment

# Configura o pydub para usar o ffmpeg específico
def configure_pydub():
    """Configura o pydub para usar o ffmpeg específico"""
    import platform
    
    if platform.system() == "Windows":
        ffmpeg_path = os.path.expanduser("~/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-7.1.1-full_build/bin")
        
        if os.path.exists(ffmpeg_path):
            AudioSegment.converter = os.path.join(ffmpeg_path, "ffmpeg.exe")
            AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
            AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")

# Configura o pydub
configure_pydub()

def get_file_size_mb(file_path):
    """Retorna o tamanho do arquivo em MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def extract_audio_from_mp4(mp4_path, output_path, audio_format="M4A", bitrate=64, sample_rate=16000, mono=True):
    """Extrai áudio do arquivo MP4 otimizado para transcrição (menor tamanho)"""
    try:
        # Carrega o arquivo MP4
        audio = AudioSegment.from_file(mp4_path, format="mp4")
        
        # Mostra parâmetros originais
        st.info(f"📊 Original: {audio.frame_rate}Hz, {audio.channels} canais, {audio.sample_width*8}-bit")
        
        # Aplicar configurações de otimização
        
        # 1. Sample rate (16kHz é suficiente para speech)
        if audio.frame_rate != sample_rate:
            audio = audio.set_frame_rate(sample_rate)
            st.info(f"🔄 Sample rate: {sample_rate}Hz (otimizado para voz)")
        
        # 2. Mono (reduz tamanho pela metade)
        if mono and audio.channels > 1:
            audio = audio.set_channels(1)
            st.info("🔄 Convertido para Mono (50% menor)")
        
        # 3. Determinar formato e parâmetros
        format_config = {
            "M4A": {
                "format": "mp4",
                "extension": ".m4a", 
                "codec": "aac",
                "params": ["-c:a", "aac", "-b:a", f"{bitrate}k"]
            },
            "MP3": {
                "format": "mp3",
                "extension": ".mp3",
                "codec": "mp3", 
                "params": ["-c:a", "mp3", "-b:a", f"{bitrate}k"]
            },
            "WEBM": {
                "format": "webm",
                "extension": ".webm",
                "codec": "opus",
                "params": ["-c:a", "libopus", "-b:a", f"{bitrate}k"]
            },
            "MPGA": {
                "format": "mp3", 
                "extension": ".mpga",
                "codec": "mp3",
                "params": ["-c:a", "mp3", "-b:a", f"{bitrate}k"]
            },
            "WAV": {
                "format": "wav",
                "extension": ".wav",
                "codec": "pcm",
                "params": ["-c:a", "pcm_s16le"]
            }
        }
        
        config = format_config[audio_format]
        
        # Atualiza o caminho com a extensão correta
        output_path = output_path.replace(".wav", config["extension"])
        
        # Parâmetros base
        export_params = [
            "-ar", str(sample_rate),
            "-ac", "1" if mono else "2"
        ] + config["params"]
        
        # Exporta otimizado
        audio.export(
            output_path,
            format=config["format"],
            parameters=export_params
        )
        
        return output_path
        
    except Exception as e1:
        st.warning(f"Método pydub falhou: {str(e1)}")
        
        # Método 2: FFmpeg direto (mais eficiente)
        try:
            config = {
                "M4A": ["-c:a", "aac", "-b:a", f"{bitrate}k"],
                "MP3": ["-c:a", "mp3", "-b:a", f"{bitrate}k"], 
                "WEBM": ["-c:a", "libopus", "-b:a", f"{bitrate}k"],
                "MPGA": ["-c:a", "mp3", "-b:a", f"{bitrate}k"],
                "WAV": ["-c:a", "pcm_s16le"]
            }
            
            extensions = {
                "M4A": ".m4a", "MP3": ".mp3", "WEBM": ".webm", 
                "MPGA": ".mpga", "WAV": ".wav"
            }
            
            output_path = output_path.replace(".wav", extensions[audio_format])
            
            cmd = [
                'ffmpeg', '-i', mp4_path,
                '-vn',  # Sem vídeo
                '-ar', str(sample_rate),
                '-ac', '1' if mono else '2',
                '-y', output_path
            ] + config[audio_format]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return output_path
            else:
                st.error(f"Erro no ffmpeg: {result.stderr}")
                return None
                
        except Exception as e2:
            st.error(f"Erro no método FFmpeg: {str(e2)}")
            return None

def split_audio_file(audio_path, max_size_mb=20):
    """Divide o arquivo de áudio em chunks de tamanho específico"""
    try:
        # Carrega o arquivo de áudio
        audio = AudioSegment.from_file(audio_path)
        
        # Calcula o tamanho atual em MB
        current_size_mb = get_file_size_mb(audio_path)
        
        if current_size_mb <= max_size_mb:
            return [audio_path]  # Não precisa dividir
        
        # Calcula quantos chunks serão necessários
        num_chunks = math.ceil(current_size_mb / max_size_mb)
        
        # Calcula a duração de cada chunk em milissegundos
        chunk_duration_ms = len(audio) // num_chunks
        
        # Nome base do arquivo
        base_name = Path(audio_path).stem
        extension = Path(audio_path).suffix
        base_dir = Path(audio_path).parent
        
        chunks_paths = []
        
        for i in range(num_chunks):
            start_ms = i * chunk_duration_ms
            
            # Para o último chunk, vai até o final do áudio
            if i == num_chunks - 1:
                end_ms = len(audio)
            else:
                end_ms = (i + 1) * chunk_duration_ms
            
            # Extrai o chunk
            chunk = audio[start_ms:end_ms]
            
            # Define o nome do arquivo do chunk
            chunk_filename = f"{base_name}-p{i+1}{extension}"
            chunk_path = base_dir / chunk_filename
            
            # Salva o chunk no mesmo formato do arquivo original
            chunk.export(chunk_path, format=extension[1:])  # Remove o ponto da extensão
            chunks_paths.append(str(chunk_path))
        
        return chunks_paths
        
    except Exception as e:
        st.error(f"Erro ao dividir arquivo: {str(e)}")
        return []

def create_download_zip(file_paths, zip_name):
    """Cria um arquivo ZIP contendo todos os arquivos"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            zip_file.write(file_path, file_name)
    
    zip_buffer.seek(0)
    return zip_buffer

def main():
    st.title("🎵 Extrator de Áudio MP4 para WAV")
    st.markdown("---")
    
    # Informações sobre o limite de upload
    try:
        show_upload_info()
    except NameError:
        st.info("📁 **Limite de Upload**: Configurado para aceitar arquivos de até **2GB** (2024 MB)")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "Selecione um arquivo MP4",
        type=['mp4'],
        help="Carregue um arquivo de vídeo MP4 para extrair o áudio. Limite: 2GB"
    )
    
    if uploaded_file is not None:
        # Mostra informações do arquivo
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.info(f"📁 Arquivo: {uploaded_file.name}")
        st.info(f"📊 Tamanho: {file_size_mb:.2f} MB")
        
        # Opções de processamento
        st.markdown("### Opções de Processamento")
        
        # Formato otimizado para transcrição
        st.info("🎯 **Otimizado para Transcrição**: Configurações para menor tamanho possível mantendo qualidade suficiente para transcrição de texto.")
        
        audio_format = st.selectbox(
            "Formato de áudio:",
            [
                "M4A (Menor tamanho - Recomendado)", 
                "MP3 (Compatível)", 
                "WEBM (Muito pequeno)",
                "MPGA (MP3 alternativo)",
                "WAV (Maior qualidade/tamanho)"
            ],
            help="M4A oferece o melhor equilíbrio tamanho/qualidade para transcrição"
        )
        
        # Configurações otimizadas para transcrição
        st.markdown("**⚙️ Configurações para Transcrição:**")
        col1, col2 = st.columns(2)
        
        with col1:
            # Sample rate otimizado para speech
            sample_rate = st.selectbox(
                "Sample Rate:",
                [16000, 22050, 44100],
                index=0,  # 16kHz por padrão
                help="16kHz é suficiente para transcrição de voz"
            )
        
        with col2:
            # Bitrate muito baixo para transcrição
            if "WAV" not in audio_format:
                bitrate = st.selectbox(
                    "Qualidade:",
                    [32, 64, 96, 128],
                    index=1,  # 64kbps por padrão
                    help="64kbps é suficiente para transcrição"
                )
        
        # Mono para reduzir ainda mais o tamanho
        mono_audio = st.checkbox(
            "Converter para Mono (reduz tamanho em ~50%)",
            value=True,
            help="Mono é suficiente para transcrição e reduz drasticamente o tamanho"
        )
        
        split_option = st.radio(
            "Escolha o tipo de saída:",
            ["Arquivo único", "Dividir em arquivos de 20MB"],
            help="Arquivo único: gera um único arquivo\nDividir: cria múltiplos arquivos de até 20MB cada"
        )
        
        # Botão para processar
        if st.button("🎯 Extrair Áudio", type="primary"):
            # Cria um diretório temporário
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    # Salva o arquivo MP4 temporariamente
                    mp4_temp_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(mp4_temp_path, 'wb') as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Define formato baseado na seleção
                    format_mapping = {
                        "M4A (Menor tamanho - Recomendado)": ("M4A", ".m4a"),
                        "MP3 (Compatível)": ("MP3", ".mp3"),
                        "WEBM (Muito pequeno)": ("WEBM", ".webm"),
                        "MPGA (MP3 alternativo)": ("MPGA", ".mpga"),
                        "WAV (Maior qualidade/tamanho)": ("WAV", ".wav")
                    }
                    
                    format_param, extension = format_mapping[audio_format]
                    audio_filename = Path(uploaded_file.name).stem + extension
                    audio_temp_path = os.path.join(temp_dir, audio_filename)
                    
                    # Mostra progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Extrai o áudio
                    status_text.text("Extraindo e otimizando áudio para transcrição...")
                    progress_bar.progress(30)
                    
                    # Parâmetros de otimização
                    if "WAV" in audio_format:
                        final_audio_path = extract_audio_from_mp4(
                            mp4_temp_path, audio_temp_path, format_param, 
                            sample_rate=sample_rate, mono=mono_audio
                        )
                    else:
                        final_audio_path = extract_audio_from_mp4(
                            mp4_temp_path, audio_temp_path, format_param, 
                            bitrate, sample_rate, mono_audio
                        )
                    
                    if final_audio_path:
                        progress_bar.progress(60)
                        
                        # Verifica o tamanho e calcula redução
                        audio_size_mb = get_file_size_mb(final_audio_path)
                        reduction_percent = ((file_size_mb - audio_size_mb) / file_size_mb) * 100
                        
                        st.success(f"✅ Áudio otimizado para transcrição!")
                        
                        # Mostra comparação de tamanhos com destaque
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("📊 Original", f"{file_size_mb:.1f} MB")
                        with col2:
                            st.metric("📊 Otimizado", f"{audio_size_mb:.1f} MB")
                        with col3:
                            if reduction_percent > 0:
                                st.metric("📉 Redução", f"{reduction_percent:.1f}%")
                            else:
                                st.metric("📈 Aumento", f"{abs(reduction_percent):.1f}%")
                        
                        # Mostra configurações aplicadas
                        config_info = f"🎛️ **Configurações:** {sample_rate}Hz"
                        if not "WAV" in audio_format:
                            config_info += f", {bitrate}kbps"
                        config_info += f", {'Mono' if mono_audio else 'Stereo'}"
                        st.info(config_info)
                        
                        # Processamento baseado na opção escolhida
                        if split_option == "Arquivo único":
                            progress_bar.progress(100)
                            status_text.text("Processamento concluído!")
                            
                            # Determina o MIME type
                            mime_types = {
                                "M4A": "audio/mp4",
                                "MP3": "audio/mpeg", 
                                "WEBM": "audio/webm",
                                "MPGA": "audio/mpeg",
                                "WAV": "audio/wav"
                            }
                            
                            # Botão de download para arquivo único
                            with open(final_audio_path, 'rb') as f:
                                st.download_button(
                                    label=f"📥 Baixar {format_param} Otimizado",
                                    data=f.read(),
                                    file_name=os.path.basename(final_audio_path),
                                    mime=mime_types[format_param],
                                    type="primary"
                                )
                        
                        else:  # Dividir em arquivos de 20MB
                            status_text.text("Dividindo arquivo em chunks...")
                            progress_bar.progress(80)
                            
                            chunks_paths = split_audio_file(final_audio_path, max_size_mb=20)
                            
                            if chunks_paths:
                                progress_bar.progress(100)
                                status_text.text("Processamento concluído!")
                                
                                # Mostra informações dos chunks
                                st.markdown("### 📂 Arquivos Gerados")
                                for i, chunk_path in enumerate(chunks_paths, 1):
                                    chunk_size = get_file_size_mb(chunk_path)
                                    chunk_name = os.path.basename(chunk_path)
                                    st.write(f"**{chunk_name}** - {chunk_size:.2f} MB")
                                
                                # Cria ZIP para download
                                zip_name = f"{Path(uploaded_file.name).stem}_audio_chunks.zip"
                                zip_buffer = create_download_zip(chunks_paths, zip_name)
                                
                                # Botão de download para ZIP
                                st.download_button(
                                    label="📥 Baixar todos os arquivos (ZIP)",
                                    data=zip_buffer.getvalue(),
                                    file_name=zip_name,
                                    mime="application/zip",
                                    type="primary"
                                )
                    
                    else:
                        st.error("❌ Falha ao extrair áudio do vídeo")
                        
                except Exception as e:
                    st.error(f"❌ Erro durante o processamento: {str(e)}")
                
                finally:
                    # Limpa a barra de progresso
                    progress_bar.empty()
                    status_text.empty()
    
    # Informações adicionais
    st.markdown("---")
    st.markdown("### ℹ️ Informações")
    st.markdown("""
    **Como usar:**
    1. Faça upload de um arquivo MP4 (até 1GB)
    2. Escolha se deseja um arquivo único ou dividido em chunks de 20MB
    3. Clique em "Extrair Áudio"
    4. Baixe o(s) arquivo(s) gerado(s)
    
    **Formatos suportados:**
    - 📥 Entrada: MP4 (até 1GB)
    - 📤 Saída: M4A, MP3, WEBM, MPGA, WAV
    
    **Recomendações para transcrição:**
    - **M4A 64kbps**: Menor tamanho, ideal para transcrição
    - **MP3 64kbps**: Boa compatibilidade, tamanho pequeno
    - **WEBM 64kbps**: Muito pequeno, formato moderno
    - **WAV**: Qualidade máxima, arquivo grande
    
    **Tamanhos aproximados (1 hora de áudio):**
    - M4A 64kbps: ~28MB
    - MP3 64kbps: ~28MB
    - WEBM 64kbps: ~25MB
    - WAV 16kHz: ~115MB
    
    **Configuração de Limite:**
    - ✅ Limite de upload: **2GB** (2024 MB)
    - ✅ Configurado via `.streamlit/config.toml`
    - ✅ Otimizado para arquivos grandes de reunião
    """)

if __name__ == "__main__":
    main()