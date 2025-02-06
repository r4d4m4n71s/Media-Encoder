@echo off

:: Enable logging
set "LOGFILE=%~dp0ffmpeg_install.log"
echo FFmpeg Installation Started: %date% %time% > "%LOGFILE%"

:: Check if FFmpeg is available in current PATH
set "FFMPEG_PATH="
for %%I in (ffmpeg.exe) do set "FFMPEG_PATH=%%~$PATH:I"

if defined FFMPEG_PATH (
    echo FFmpeg is already available in your current environment at:
    echo %FFMPEG_PATH%
    echo.
    ffmpeg -version
    echo.
    echo If you still want to proceed with the installation, press any key...
    pause >nul
)

:: Determine if we're installing from desktop or virtual environment
set "INSTALL_FROM_DESKTOP=0"
if "%~dp0"=="%USERPROFILE%\Desktop\" set "INSTALL_FROM_DESKTOP=1"
if "%~dp0"=="%USERPROFILE%\OneDrive\Desktop\" set "INSTALL_FROM_DESKTOP=1"

:: If installing from desktop, ignore any virtual environment
if "%INSTALL_FROM_DESKTOP%"=="1" (
    echo Installing from desktop - ignoring any virtual environment
    set "INSTALL_DIR=%~dp0build"
    set "VIRTUAL_ENV="
) else if defined VIRTUAL_ENV (
    echo Installing in virtual environment: %VIRTUAL_ENV%
    set "INSTALL_DIR=%VIRTUAL_ENV%"
) else (
    echo Installing in local project environment
    set "INSTALL_DIR=%~dp0build"
)

set "FFMPEG_DIR=%INSTALL_DIR%\ffmpeg"
set "TEMP_DIR=%INSTALL_DIR%\temp"
set "CMDS_DIR=%USERPROFILE%\ffmpeg-cmd"

echo Working Directory: %~dp0 >> "%LOGFILE%"
echo Installation Directory: %INSTALL_DIR% >> "%LOGFILE%"
echo FFMPEG_DIR: %FFMPEG_DIR% >> "%LOGFILE%"

echo FFmpeg Installation Script
echo ==========================
echo Installation log will be saved to: %LOGFILE%
echo.

:: Create base directories
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%CMDS_DIR%" mkdir "%CMDS_DIR%"

:: Check if FFmpeg is already installed
if exist "%FFMPEG_DIR%\bin\ffmpeg.exe" (
    echo FFmpeg is already installed in %FFMPEG_DIR%
    "%FFMPEG_DIR%\bin\ffmpeg.exe" -version
    goto CreateFiles
)

:: Create directories
echo Creating directories...
echo Attempting to create directories >> "%LOGFILE%"

if not exist "%FFMPEG_DIR%" (
    mkdir "%FFMPEG_DIR%" 2>>"%LOGFILE%" || (
        echo Failed to create directory: %FFMPEG_DIR%
        echo Failed to create FFMPEG_DIR >> "%LOGFILE%"
        pause
        exit /b 1
    )
)

if not exist "%TEMP_DIR%" (
    mkdir "%TEMP_DIR%" 2>>"%LOGFILE%" || (
        echo Failed to create directory: %TEMP_DIR%
        echo Failed to create TEMP_DIR >> "%LOGFILE%"
        pause
        exit /b 1
    )
)

:: Download FFmpeg using PowerShell
echo Downloading FFmpeg...
echo Downloading FFmpeg >> "%LOGFILE%"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference = 'SilentlyContinue'; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $url = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'; $output = Join-Path '%TEMP_DIR%' 'ffmpeg.zip'; Write-Host 'Downloading FFmpeg...'; try { Invoke-WebRequest -Uri $url -OutFile $output; Write-Host 'Download completed successfully'; } catch { Write-Host 'Download failed: $_'; exit 1; }"

if not exist "%TEMP_DIR%\ffmpeg.zip" (
    echo FFmpeg download failed - file not found
    echo Download failed - file not found >> "%LOGFILE%"
    pause
    exit /b 1
)

:: Extract FFmpeg using PowerShell
echo Extracting FFmpeg...
echo Extracting FFmpeg >> "%LOGFILE%"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference = 'SilentlyContinue'; Add-Type -AssemblyName System.IO.Compression.FileSystem; $zipPath = Join-Path '%TEMP_DIR%' 'ffmpeg.zip'; $extractPath = '%TEMP_DIR%'; Write-Host 'Extracting FFmpeg...'; try { [System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $extractPath); Write-Host 'Extraction completed successfully'; } catch { Write-Host 'Extraction failed: $_'; exit 1; }"

:: Move FFmpeg files to the correct location
echo Moving FFmpeg files...
echo Moving FFmpeg files >> "%LOGFILE%"

:: Create bin directory
if not exist "%FFMPEG_DIR%\bin" mkdir "%FFMPEG_DIR%\bin"

:: Find the extracted directory and copy files
for /d %%i in ("%TEMP_DIR%\ffmpeg-*") do (
    xcopy "%%i\bin\*" "%FFMPEG_DIR%\bin\" /E /I /Y >>"%LOGFILE%" 2>&1
)

:: Clean up
echo Cleaning up temporary files...
echo Cleaning up >> "%LOGFILE%"
rd /s /q "%TEMP_DIR%" 2>>"%LOGFILE%"

:CreateFiles
:: Create command shortcuts in user's home directory
echo Creating command shortcuts in %CMDS_DIR%...

:: Create ffmpeg.cmd
(
    echo @echo off
    echo "%FFMPEG_DIR%\bin\ffmpeg.exe" %%*
) > "%CMDS_DIR%\ffmpeg.cmd"

:: Create ffprobe.cmd
(
    echo @echo off
    echo "%FFMPEG_DIR%\bin\ffprobe.exe" %%*
) > "%CMDS_DIR%\ffprobe.cmd"

:: Handle PATH setup based on installation type
if "%INSTALL_FROM_DESKTOP%"=="1" (
    :: Add FFmpeg to system PATH for desktop installation
    echo Adding FFmpeg to system PATH...
    echo Adding FFmpeg to system PATH >> "%LOGFILE%"
    
    powershell -NoProfile -ExecutionPolicy Bypass -Command "$ffmpegPath = '%FFMPEG_DIR%\bin'; $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'Machine'); if ($currentPath -notlike '*' + $ffmpegPath + '*') { $newPath = $currentPath + ';' + $ffmpegPath; [Environment]::SetEnvironmentVariable('PATH', $newPath, 'Machine'); Write-Host 'FFmpeg added to system PATH successfully' } else { Write-Host 'FFmpeg path already exists in system PATH' }"
) else if defined VIRTUAL_ENV (
    :: Create and execute activate.bat for virtual environment
    echo Setting up FFmpeg in virtual environment...
    echo Setting up FFmpeg in virtual environment >> "%LOGFILE%"
    
    (
        echo @echo off
        echo set "PATH=%FFMPEG_DIR%\bin;%%PATH%%"
        echo echo FFmpeg environment activated. Run 'ffmpeg -version' to verify.
    ) > "%INSTALL_DIR%\activate.bat"
    
    :: Automatically execute activate.bat
    echo Activating FFmpeg in virtual environment...
    call "%INSTALL_DIR%\activate.bat"
) else (
    :: Create local activate.bat for project environment
    echo Setting up FFmpeg in local project environment...
    echo Setting up FFmpeg in local project environment >> "%LOGFILE%"
    
    (
        echo @echo off
        echo set "PATH=%FFMPEG_DIR%\bin;%%PATH%%"
        echo echo FFmpeg environment activated. Run 'ffmpeg -version' to verify.
    ) > "%INSTALL_DIR%\activate.bat"
)

echo.
echo Installation completed successfully!
echo.
echo FFmpeg has been installed to: %FFMPEG_DIR%\bin

if "%INSTALL_FROM_DESKTOP%"=="1" (
    echo Desktop installation detected
    echo FFmpeg is now available system-wide
) else if defined VIRTUAL_ENV (
    echo Virtual environment detected: %VIRTUAL_ENV%
    echo FFmpeg has been automatically activated in your virtual environment
    ffmpeg -version
) else (
    echo Local project installation detected
    echo To use FFmpeg, run '%INSTALL_DIR%\activate.bat' to add it to your PATH
)
echo.
echo Command shortcuts are available at: %CMDS_DIR%
echo.

pause
exit /b 0