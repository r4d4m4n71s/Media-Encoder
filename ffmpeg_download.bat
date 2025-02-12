if exist "build\ffmpeg.exe" (
    if exist "build\ffprobe.exe" (
        if exist "build\ffplay.exe" (
            echo FFmpeg tools already installed in build folder.
            goto :skip_download
        )
    )
)

echo Creating build directory...
if not exist "build" mkdir build

echo Downloading ffmpeg...
powershell -Command "& {$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'build\ffmpeg.zip'}"

echo Extracting all exe files...
powershell -Command "& {Add-Type -AssemblyName System.IO.Compression.FileSystem; $zip = [System.IO.Compression.ZipFile]::OpenRead('build\ffmpeg.zip'); $zip.Entries | Where-Object { $_.Name -like '*.exe' -and $_.FullName -like '*bin*' } | ForEach-Object { [System.IO.Compression.ZipFileExtensions]::ExtractToFile($_, ('build\' + $_.Name), $true) }; $zip.Dispose()}"

echo Cleaning up...
del "build\ffmpeg.zip"

:skip_download
echo Build completed successfully!