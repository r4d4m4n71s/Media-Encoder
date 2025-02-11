if exist "dist\ffmpeg.exe" (
    if exist "dist\ffprobe.exe" (
        if exist "dist\ffplay.exe" (
            echo FFmpeg tools already installed in dist folder.
            goto :skip_download
        )
    )
)

echo Creating dist directory...
if not exist "dist" mkdir dist

echo Downloading ffmpeg...
powershell -Command "& {$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'dist\ffmpeg.zip'}"

echo Extracting all exe files...
powershell -Command "& {Add-Type -AssemblyName System.IO.Compression.FileSystem; $zip = [System.IO.Compression.ZipFile]::OpenRead('dist\ffmpeg.zip'); $zip.Entries | Where-Object { $_.Name -like '*.exe' -and $_.FullName -like '*bin*' } | ForEach-Object { [System.IO.Compression.ZipFileExtensions]::ExtractToFile($_, ('dist\' + $_.Name), $true) }; $zip.Dispose()}"

echo Cleaning up...
del "dist\ffmpeg.zip"

:skip_download
echo Build completed successfully!