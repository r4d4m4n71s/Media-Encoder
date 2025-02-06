#!/bin/bash

# Help message
show_help() {
    echo "Media Encoder Build Script"
    echo
    echo "Usage: ./build.sh [target]"
    echo
    echo "Build Targets:"
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
    echo "  ./build.sh local   - Set up for development"
    echo "  ./build.sh release - Create distribution packages"
    echo "  ./build.sh encoder - Build encoder executable"
}

# Make script executable
chmod +x install_ffmpeg.sh

case "$1" in
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
        
        # Install FFmpeg first
        echo "Installing FFmpeg..."
        ./install_ffmpeg.sh || exit 1
        
        # Create required directories
        CMDS_DIR="$HOME/.local/bin"
        mkdir -p "$CMDS_DIR"
        mkdir -p dist/encoder/
        
        # Install core requirements first
        echo "Installing core requirements..."
        python3 -m pip install -r src/requirements.txt || exit 1
        
        # Install development dependencies
        echo "Installing development dependencies..."
        python3 -m pip install -r requirements-dev.txt || exit 1
        
        # Clean previous builds
        rm -rf dist/encoder/ build/encoder/
        
        # Build executable using spec file
        python3 -m PyInstaller --clean encoder.spec || exit 1
        
        # Move the executable and copy FFmpeg
        mv dist/encoder dist/encoder/ || exit 1
        
        # Create command shortcut
        ENCODER_PATH="$(pwd)/dist/encoder/encoder"
        echo '#!/bin/bash' > "$CMDS_DIR/encoder"
        echo "\"$ENCODER_PATH\" \"\$@\"" >> "$CMDS_DIR/encoder"
        chmod +x "$CMDS_DIR/encoder"
        
        # Copy FFmpeg to distribution directory if available
        if command -v ffmpeg &> /dev/null; then
            FFMPEG_PATH=$(command -v ffmpeg)
            echo "Copying FFmpeg to distribution directory..."
            cp "$FFMPEG_PATH" "dist/encoder/" || exit 1
        fi
        
        echo
        echo "Encoder executable built successfully"
        echo "Available at dist/encoder/encoder"
        echo
        echo "Command shortcut created at: $CMDS_DIR/encoder"
        if [[ ":$PATH:" != *":$CMDS_DIR:"* ]]; then
            echo "Add $CMDS_DIR to your PATH to use 'encoder' from any location"
        fi
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
