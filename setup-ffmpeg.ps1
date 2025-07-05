# Script para configurar o ffmpeg no PATH permanentemente
# Execute este script como administrador

$ffmpegPath = "C:\Users\$env:USERNAME\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1.1-full_build\bin"

# Verificar se o diretório existe
if (Test-Path $ffmpegPath) {
    Write-Host "FFmpeg encontrado em: $ffmpegPath" -ForegroundColor Green
    
    # Adicionar ao PATH do usuário
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    
    if ($currentPath -notlike "*$ffmpegPath*") {
        $newPath = $currentPath + ";" + $ffmpegPath
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Host "FFmpeg adicionado ao PATH do usuário" -ForegroundColor Green
    } else {
        Write-Host "FFmpeg já está no PATH do usuário" -ForegroundColor Yellow
    }
    
    # Testar se funciona
    Write-Host "Testando ffmpeg..." -ForegroundColor Cyan
    & "$ffmpegPath\ffmpeg.exe" -version | Select-Object -First 1
    
    Write-Host "`nConfiguração concluída! Reinicie o terminal para aplicar as mudanças." -ForegroundColor Green
} else {
    Write-Host "FFmpeg não encontrado em: $ffmpegPath" -ForegroundColor Red
    Write-Host "Certifique-se de que o FFmpeg foi instalado via winget" -ForegroundColor Yellow
} 