@echo off
setlocal

if "%1"=="" goto help
if "%1"=="local" goto local
if "%1"=="release" goto release
if "%1"=="deploy" goto deploy
if "%1"=="encoder" goto encoder
if "%1"=="help" goto help

:help
echo Media Encoder Build Script
echo.
echo Usage: build.bat [target]
echo.
echo Build Targets:
echo   local   - Set up local development environment
echo            * Installs core dependencies
echo            * Installs development dependencies
echo            * Installs package in editable mode
echo.
echo   release - Build release packages
echo            * Cleans previous builds
echo            * Runs test suite with coverage
echo            * Creates wheel and source distributions
echo            * Output available in dist/ directory
echo.
echo   deploy  - Deploy to PyPI using twine
echo            * Uploads built packages to PyPI
echo            * Requires PyPI credentials
echo            * Must run 'release' target first
echo.
echo   encoder - Build encoder executable
echo            * Creates encoder.exe using PyInstaller
echo            * Output available in dist/ directory
echo.
echo   help    - Show this help message
echo.
echo Examples:
echo   build.bat local   - Set up for development
echo   build.bat release - Create distribution packages
echo   build.bat encoder - Build encoder executable
goto :eof

:local
echo === Setting up local development environment ===
python -m pip install -r src/requirements.txt
if %errorlevel% neq 0 exit /b %errorlevel%

python -m pip install -r requirements-dev.txt
if %errorlevel% neq 0 exit /b %errorlevel%

python -m pip install -e .
if %errorlevel% neq 0 exit /b %errorlevel%

echo Local development environment ready
goto :eof

:release
echo === Building release packages ===
rem Clean previous builds
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "*.egg-info" rd /s /q "*.egg-info"

rem Run tests
python -m pytest tests -v --cov=src
if %errorlevel% neq 0 exit /b %errorlevel%

rem Build packages
python -m build --wheel --sdist
if %errorlevel% neq 0 exit /b %errorlevel%

echo Release packages built successfully
echo Artifacts available in the 'dist' directory
goto :eof

:deploy
echo === Deploying to PyPI ===
if not exist "dist" (
    echo No distribution files found. Run 'build.bat release' first.
    exit /b 1
)

echo Uploading to PyPI...
python -m twine upload dist/*
if %errorlevel% neq 0 exit /b %errorlevel%

echo Deployment complete
goto :eof

:encoder
echo === Building encoder executable ===
rem Clean previous builds
if exist "dist\encoder" rd /s /q "dist\encoder"
if exist "build\encoder" rd /s /q "build\encoder"

rem Build executable
python -m PyInstaller --clean ^
    --name encoder ^
    --onefile ^
    --distpath dist\encoder ^
    --workpath build\encoder ^
    --add-data "src/config/ffmpeg.audio.profiles.json;config" ^
    src/encoder_cli.py

if %errorlevel% neq 0 exit /b %errorlevel%

echo Encoder executable built successfully
echo Available at dist\encoder\encoder.exe
