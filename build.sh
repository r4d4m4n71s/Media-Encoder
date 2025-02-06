#!/bin/bash

# Help message
show_help() {
    echo "Media Encoder Build Script"
    echo
    echo "Usage: ./build.sh [target]"
    echo
    echo "Build Targets:"
    echo "  user    - Install for regular users"
    echo "           * Installs FFmpeg if not present"
    echo "           * Installs core dependencies only"
    echo "           * Installs package in regular mode"
    echo
    echo "  local   - Set up local development environment"
    echo "           * Installs FFmpeg if not present"
    echo "           * Installs core dependencies"
    echo "           * Installs development dependencies"
    echo "           * Installs package in editable mode"
    echo
    echo "  release - Build release packages"
    echo "           * Cleans previous builds"
    echo "           * Runs test suite with coverage"
    echo "           * Creates wheel and source distributions"
    echo "           * Output available in dist/ directory"
    echo
    echo "  deploy  - Deploy to PyPI using twine"
    echo "           * Uploads built packages to PyPI"
    echo "           * Requires PyPI credentials"
    echo "           * Must run 'release' target first"
    echo
    echo "  encoder - Build encoder executable"
    echo "           * Installs FFmpeg if not present"
    echo "           * Creates encoder executable using PyInstaller"
    echo "           * Output available in dist/ directory"
    echo
    echo "  help    - Show this help message"
    echo
    echo "Examples:"
    echo "  ./build.sh user    - Install for regular use"
    echo "  ./build.sh local   - Set up for development"
    echo "  ./build.sh release - Create distribution packages"
    echo "  ./build.sh encoder - Build encoder executable"
}

# Make script executable
chmod +x install_ffmpeg.sh

case "$1" in
    "user")
        echo "=== Installing for regular users ==="
        if ! command -v ffmpeg &> /dev/null; then
            echo "Installing FFmpeg..."
            ./install_ffmpeg.sh || exit 1
        fi
        
        python3 -m pip install -r src/requirements.txt || exit 1
        python3 -m pip install . || exit 1
        echo "Regular installation complete"
        ;;
        
    "local")
        echo "=== Setting up local development environment ==="
        if ! command -v ffmpeg &> /dev/null; then
            echo "Installing FFmpeg..."
            ./install_ffmpeg.sh || exit 1
        fi
        
        python3 -m pip install -r src/requirements.txt || exit 1
        python3 -m pip install -r requirements-dev.txt || exit 1
        python3 -m pip install -e .[dev] || exit 1
        echo "Local development environment ready"
        ;;
        
    "release")
        echo "=== Building release packages ==="
        # Clean previous builds
        rm -rf dist/ build/ *.egg-info/
        
        # Run tests
        python3 -m pytest tests -v --cov=src || exit 1
        
        # Build packages
        python3 -m build --wheel --sdist || exit 1
        
        echo "Release packages built successfully"
        echo "Artifacts available in the 'dist' directory"
        ;;
        
    "deploy")
        echo "=== Deploying to PyPI ==="
        if [ ! -d "dist" ]; then
            echo "No distribution files found. Run './build.sh release' first."
            exit 1
        fi
        
        echo "Uploading to PyPI..."
        python3 -m twine upload dist/* || exit 1
        echo "Deployment complete"
        ;;
        
    "encoder")
        echo "=== Building encoder executable ==="
        if ! command -v ffmpeg &> /dev/null; then
            echo "Installing FFmpeg..."
            ./install_ffmpeg.sh || exit 1
        fi
        
        # Clean previous builds
        rm -rf dist/encoder/ build/encoder/
        
        # Build executable using spec file
        python3 -m PyInstaller --clean encoder.spec || exit 1
        
        # Move the executable to the correct location
        mkdir -p dist/encoder/
        mv dist/encoder dist/encoder/
        
        echo "Encoder executable built successfully"
        echo "Available at dist/encoder/encoder"
        ;;
        
    "help"|"")
        show_help
        ;;
        
    *)
        echo "Unknown target: $1"
        echo "Run './build.sh help' for usage information"
        exit 1
        ;;
esac
