# Media Encoder

A media encoding tool supporting various audio formats and streaming service profiles.

## Description

Media Encoder is a Python-based tool designed to handle media encoding tasks, with a focus on audio format conversion and streaming service profile support. It provides a flexible and user-friendly interface for managing your media encoding needs.

## Features

- Audio format conversion with multiple codec support (MP3, FLAC, ALAC, WAV, Opus)
- Streaming service profile support for major platforms (Spotify, Apple Music, Tidal, etc.)
- JSON-based configuration for encoding profiles
- Command-line interface for easy automation
- Standalone encoder executable
- Detailed profile information including size and CPU usage factors
- Cross-platform support

## Profiles

{profiles_table}

## Usage

### Command Line Interface
After installation, you can use the tool from the command line:

Basic usage:
```bash
media-encoder input.mp3 output.mp3 --profile "MP3 Standard 320kbps"
```

List all available profiles with detailed information:
```bash
media-encoder --list-profiles
```

Using a specific profile:
```bash
media-encoder input.flac output.m4a --profile "Apple Music (Lossless)"
```

## Requirements

### Core Dependencies
- Python 3.8 or higher
- loguru==0.7.3 - For logging functionality

### Development Dependencies
- pytest==7.4.3 - Testing framework
- pytest-cov==4.1.0 - Test coverage reporting
- build==1.0.3 - Package building
- wheel==0.41.2 - Package distribution
- setuptools>=65.5.1 - Package setup
- twine==4.0.2 - Package publishing
- black==23.11.0 - Code formatting
- ruff==0.1.6 - Fast Python linter
- mypy==1.7.0 - Static type checking
- pyinstaller==6.11.1 - Executable creation
- tabulate==0.9.0 - Table formatting

## Installation

### For Users
To install Media Encoder for regular use:

```bash
build.bat user
```

This will install:
- Core dependencies only
- Regular package installation

### For Developers
To set up the development environment:

```bash
build.bat local
```

This will install:
- Core dependencies
- Development tools (testing, building, linting)
- Package in editable mode

### Standalone Executable
To build the standalone encoder executable:

```bash
build.bat encoder
```

This creates `encoder.exe` in the `dist/encoder` directory. The executable can be used without Python installation:

```bash
encoder.exe input.mp3 output.mp3 --profile "MP3 Standard 320kbps"
encoder.exe --list-profiles
```

## Build Commands

- `build.bat user` - Install for regular users
- `build.bat local` - Set up development environment
- `build.bat release` - Create distribution packages
- `build.bat deploy` - Deploy to PyPI
- `build.bat encoder` - Build standalone executable
- `build.bat help` - Show help message

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

### Key Points:
- Free to use, modify, and distribute
- Must keep source code open source
- Changes must be documented
- Include original license and copyright notices
- No warranty provided

For more details, visit: https://www.gnu.org/licenses/gpl-3.0.html