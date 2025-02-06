#!/bin/bash

echo "FFmpeg Installation Script"
echo "========================="

# Function to check if a command exists in PATH
check_command() {
    command -v "$1" &> /dev/null
}

# Function to verify FFmpeg installation
verify_ffmpeg() {
    if check_command ffmpeg; then
        echo "FFmpeg is in PATH"
        echo "FFmpeg version:"
        ffmpeg -version
        return 0
    else
        echo "FFmpeg is not found in PATH"
        return 1
    fi
}

# Check if FFmpeg is already installed
if verify_ffmpeg; then
    echo "FFmpeg is already installed and working correctly!"
    exit 0
fi

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ -f /etc/os-release ]]; then
        source /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

# Function to install on macOS
install_macos() {
    echo "Installing FFmpeg on macOS..."
    
    # Check if Homebrew is installed
    if ! check_command brew; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for the current session
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    # Install FFmpeg
    brew install ffmpeg
}

# Function to install on Ubuntu/Debian
install_ubuntu() {
    echo "Installing FFmpeg on Ubuntu/Debian..."
    sudo apt update
    sudo apt install -y ffmpeg
}

# Function to install on Fedora
install_fedora() {
    echo "Installing FFmpeg on Fedora..."
    sudo dnf install -y ffmpeg
}

# Function to install on Arch Linux
install_arch() {
    echo "Installing FFmpeg on Arch Linux..."
    sudo pacman -S --noconfirm ffmpeg
}

# Main installation logic
OS=$(detect_os)
case $OS in
    "macos")
        install_macos
        ;;
    "ubuntu"|"debian")
        install_ubuntu
        ;;
    "fedora")
        install_fedora
        ;;
    "arch")
        install_arch
        ;;
    *)
        echo "Unsupported operating system"
        echo "Please install FFmpeg manually for your system"
        exit 1
        ;;
esac

# Final verification
echo -e "\nVerifying FFmpeg installation..."
if verify_ffmpeg; then
    echo -e "\nFFmpeg installed successfully!"
    exit 0
else
    echo "FFmpeg installation failed or PATH is not properly set"
    echo "Try restarting your terminal or adding FFmpeg to your PATH manually"
    exit 1
fi