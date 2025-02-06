@echo off
setlocal

if "%1"=="" goto help
if "%1"=="user" goto user
if "%1"=="local" goto local
if "%1"=="release" goto release
if "%1"=="encoder" goto encoder
if "%1"=="help" goto help

:help
echo Media Encoder Build Script
echo.
echo Usage: build.bat [target]
echo.
echo Build Targets:
echo   local   - Set up local development environment
echo            * Installs FFmpeg if not present
echo            * Installs core dependencies
echo            * Installs development dependencies
echo            * Installs package in editable mode
echo.
echo   release - Build and deploy release packages
echo            * Cleans previous builds
echo            * Runs test suite with coverage
echo            * Creates wheel and source distributions
echo            * Uploads built packages to PyPI
echo            * Requires PyPI credentials
echo.
echo   encoder - Build encoder executable
echo            * Installs FFmpeg if not present
echo            * Creates encoder.exe using PyInstaller
echo            * Output available in dist/ directory
echo.
echo   help    - Show this help message
echo.
echo Examples:
echo   build.bat local   - Set up for development
echo   build.bat release - Create and deploy distribution packages
echo   build.bat encoder - Build encoder executable
goto :eof

:user
echo === Installing for regular users ===
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing FFmpeg...
    call install_ffmpeg.bat
    if %errorlevel% neq 0 exit /b %errorlevel%
)

python -m pip install -r src/requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

python -m pip install .
if %errorlevel% neq 0 exit /b %errorlevel%

echo Regular installation complete
goto :eof

:local
echo === Setting up local development environment ===
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing FFmpeg...
    call install_ffmpeg.bat
    if %errorlevel% neq 0 exit /b %errorlevel%
)

python -m pip install -r src/requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

python -m pip install -r requirements-dev.txt
if %errorlevel% neq 0 exit /b %errorlevel%

python -m pip install -e .[dev]
if %errorlevel% neq 0 exit /b %errorlevel%

echo Local development environment ready
goto :eof

:release
echo === Building and deploying release packages ===
rem Clean previous builds
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "*.egg-info" rd /s /q "*.egg-info"

rem Run tests
python -m pytest tests -v --cov=src
if %errorlevel% neq 0 (
    echo Tests failed - cleaning up...
    if exist "dist" rd /s /q "dist"
    if exist "*.egg-info" rd /s /q "*.egg-info"
    exit /b %errorlevel%
)

rem Build packages
python -m build --wheel --sdist
if %errorlevel% neq 0 (
    echo Build failed - cleaning up...
    if exist "dist" rd /s /q "dist"
    if exist "*.egg-info" rd /s /q "*.egg-info"
    exit /b %errorlevel%
)

echo Uploading to PyPI...
python -m twine upload dist/*
if %errorlevel% neq 0 (
    echo Upload failed - cleaning up...
    if exist "dist" rd /s /q "dist"
    if exist "*.egg-info" rd /s /q "*.egg-info"
    exit /b %errorlevel%
)

rem Clean up after successful deployment
if exist "dist" rd /s /q "dist"
if exist "*.egg-info" rd /s /q "*.egg-info"

echo Release and deployment completed successfully
goto :eof

:encoder
echo === Building encoder executable ===

:: Determine if we're installing from desktop or virtual environment
set "INSTALL_FROM_DESKTOP=0"
if "%~dp0"=="%USERPROFILE%\Desktop\" set "INSTALL_FROM_DESKTOP=1"
if "%~dp0"=="%USERPROFILE%\OneDrive\Desktop\" set "INSTALL_FROM_DESKTOP=1"

:: Check FFmpeg installation
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing FFmpeg...
    call install_ffmpeg.bat
    if %errorlevel% neq 0 exit /b %errorlevel%
)

:: Install core requirements first
echo Installing core requirements...
python -m pip install -r src/requirements.txt

:: Handle additional dependencies based on installation type
if "%INSTALL_FROM_DESKTOP%"=="1" (
    echo Desktop installation detected - installing PyInstaller...
    python -m pip install pyinstaller==6.11.1
) else if defined VIRTUAL_ENV (
    echo Virtual environment detected - installing development dependencies...
    python -m pip install -r requirements-dev.txt
) else (
    echo Local project installation - installing development dependencies...
    python -m pip install -r requirements-dev.txt
)

rem Clean previous builds and temporary files
if exist "dist\encoder" rd /s /q "dist\encoder"
if exist "build\encoder" rd /s /q "build\encoder"

rem Build executable using spec file
python -m PyInstaller --clean encoder.spec

if %errorlevel% neq 0 exit /b %errorlevel%

rem Create required directories
if not exist "dist\encoder" mkdir "dist\encoder"
set "CMDS_DIR=%USERPROFILE%\ffmpeg-cmd"
if not exist "%CMDS_DIR%" mkdir "%CMDS_DIR%"

rem Move the executable and FFmpeg to the correct location
move /Y "dist\encoder.exe" "dist\encoder\"
copy /Y "build\ffmpeg\bin\ffmpeg.exe" "dist\encoder\"

rem Install FFmpeg first
echo Installing FFmpeg...
call install_ffmpeg.bat
if %errorlevel% neq 0 exit /b %errorlevel%

rem Wait for FFmpeg installation to complete
timeout /t 2 /nobreak >nul

rem Get absolute paths
set "ENCODER_PATH=%CD%\dist\encoder\encoder.exe"
set "FFMPEG_PATH=%CD%\build\ffmpeg\bin\ffmpeg.exe"

rem Create encoder command shortcut with absolute path
(
    echo @echo off
    echo "%ENCODER_PATH%" %%*
) > "%CMDS_DIR%\encoder.cmd"

rem Copy FFmpeg files after ensuring they exist
if exist "%CD%\build\ffmpeg\bin\ffmpeg.exe" (
    echo Copying FFmpeg to distribution directory...
    copy /Y "%CD%\build\ffmpeg\bin\ffmpeg.exe" "dist\encoder\"
) else (
    echo Error: FFmpeg files not found after installation
    exit /b 1
)

rem Add CMDS_DIR to system PATH if not already present
powershell -NoProfile -ExecutionPolicy Bypass -Command "$cmdsPath = '%CMDS_DIR%'; $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User'); if ($currentPath -notlike '*' + $cmdsPath + '*') { $newPath = $currentPath + ';' + $cmdsPath; [Environment]::SetEnvironmentVariable('PATH', $newPath, 'User'); Write-Host 'Added command directory to user PATH' } else { Write-Host 'Command directory already in PATH' }"

rem Clean up temporary build files
if exist "build\encoder" rd /s /q "build\encoder"

echo.
echo Encoder executable built successfully
if "%INSTALL_FROM_DESKTOP%"=="1" (
    echo Desktop build completed - executable available at:
) else if defined VIRTUAL_ENV (
    echo Virtual environment build completed - executable available at:
) else (
    echo Local project build completed - executable available at:
)
echo dist\encoder\encoder.exe
echo.
echo Note: Temporary build files have been cleaned up
echo FFmpeg has been included in the distribution directory
echo.
echo Command shortcut created at: %CMDS_DIR%\encoder.cmd
echo Add %CMDS_DIR% to your PATH to use 'encoder' from any location
goto :eof