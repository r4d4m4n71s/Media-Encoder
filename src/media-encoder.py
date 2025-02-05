import argparse
import sys
import os
import tempfile
import shutil
from pathlib import Path
from tabulate import tabulate
from data_manager import ProfilesDataManager
from models import Profile
from __init__ import FFMPEG_PROFILES_PATH


def read_readme():
    """Read and return the content of README.md file"""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading README.md: {str(e)}"


def create_audio_profile_table(data: list[Profile]) -> str:
    headers = ["Profile", "Codec", "Extension", "FFmpeg Setup", "Size Factor", "CPU Factor", "Description"]
    rows = []
    for profile in data:
        rows.append([
            profile.Profile,
            profile.Codec,
            profile.Extension,
            profile.FFmpegSetup,
            profile.SizeFactor,
            profile.CpuFactor,
            profile.Description
        ])
    return tabulate(rows, headers, tablefmt="github")


def create_readme(profiles_data: list[Profile]):
    # Create the profiles table
    profiles_table = create_audio_profile_table(profiles_data)
    
    # Build the complete README content
    content = f"""# Media Encoder

## Description
A powerful audio format converter with streaming service profiles support. This tool allows you to convert audio files to various formats optimized for different streaming platforms and services.

## Available Audio Profiles
Below is a list of available audio profiles with their specifications:

{profiles_table}

## Installation
To install the Media Encoder:

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r src/requirements.txt
   ```
3. Ensure you have FFmpeg installed on your system
   - Windows: Download from https://ffmpeg.org/download.html
   - Linux: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`

## Usage
### Basic Usage
```bash
python media-encoder.py <input_file> -o <output_file> -p <profile>
```

### Command Arguments
- `input_file`: Path to the input audio file
- `-o, --output`: Path for the output converted file
- `-p, --profile`: Audio profile to use for conversion (see profiles table above)

### Help Commands
- `--help`: Show this help message and basic usage information
- `--help-profiles`: Show detailed information about available audio profiles
- `--advanced-help`: Show advanced usage examples and configuration options

### Examples
1. Convert an audio file using a specific profile:
   ```bash
   python media-encoder.py input.mp3 -o output.m4a -p "Apple Music (Lossless)"
   ```

2. View available profiles:
   ```bash
   python media-encoder.py --help-profiles
   ```

3. Get detailed help:
   ```bash
   python media-encoder.py --help
   ```

## License
This project is licensed under the GNU General Public License v3.0

Permissions:
- Commercial use
- Distribution
- Modification
- Patent use
- Private use

See the LICENSE file for full details."""

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', newline='\n') as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name

    # Get the final README path
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")

    # Copy the temporary file to the final location
    shutil.copy2(temp_path, readme_path)

    # Clean up the temporary file
    os.unlink(temp_path)


def main():
    parser = argparse.ArgumentParser(description="Media Encoder - Audio format converter with streaming service profiles")
    
    # Main arguments
    parser.add_argument("input", nargs="?", help="Input audio file path")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-p", "--profile", help="Audio profile to use for conversion")
    
    # Help commands
    parser.add_argument("--help-profiles", action="store_true", help="Show available audio profiles and their details")
    parser.add_argument("--advanced-help", action="store_true", help="Show advanced usage information and examples")
    
    if len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv:
        print(read_readme())
        sys.exit(0)
        
    args = parser.parse_args()
    
    if args.help_profiles:
        data = ProfilesDataManager(FFMPEG_PROFILES_PATH).get_all_profiles()
        print(create_audio_profile_table(data))
        sys.exit(0)
        
    if args.advanced_help:
        # TODO: Implement advanced help
        print("Advanced help not implemented yet")
        sys.exit(0)
    
    # If no special flags are used, generate/update the README
    profiles_data = ProfilesDataManager(FFMPEG_PROFILES_PATH).get_all_profiles()
    print("Generating readme!...")
    create_readme(profiles_data)
    print("README.md file has been created successfully!")


if __name__ == "__main__":
    main()
