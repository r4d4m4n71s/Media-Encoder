@echo off
echo Installing dependencies...
python -m pip install -r requirements-dev.txt

echo Creating dist directory...
if not exist "dist" mkdir dist

if exist "dist\ffmpeg.exe" (
    echo FFmpeg already installed in dist folder.
) else (
    echo Downloading ffmpeg...
    powershell -Command "& {$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'dist\ffmpeg.zip'}"

    echo Extracting ffmpeg.exe...
    powershell -Command "& {Add-Type -AssemblyName System.IO.Compression.FileSystem; $zip = [System.IO.Compression.ZipFile]::OpenRead('dist\ffmpeg.zip'); $entry = $zip.Entries | Where-Object { $_.Name -eq 'ffmpeg.exe' -and $_.FullName -like '*bin*' }; [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, 'dist\ffmpeg.exe', $true); $zip.Dispose()}"

    echo Cleaning up...
    del "dist\ffmpeg.zip"
)

echo Build completed successfully!