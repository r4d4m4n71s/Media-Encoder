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

| Profile                                 | Codec      | Extension   | FFmpeg Setup                                                 |   Size Factor |   CPU Factor | Description                                    |
|-----------------------------------------|------------|-------------|--------------------------------------------------------------|---------------|--------------|------------------------------------------------|
| MP3 Standard 320kbps                    | MP3        | .mp3        | acodec=libmp3lame, b:a=320k, ar=44100                        |           1   |          1   | Standard-quality MP3, 320kbps                  |
| Apple Music (Lossless)                  | ALAC       | .m4a        | acodec=alac, ar=44100, sample_fmt=s16                        |           1   |          1.1 | Standard lossless audio                        |
| WAV (24-bit, 44.1 kHz)                  | WAV        | .wav        | acodec=pcm_s24le, ar=44100, sample_fmt=s32                   |           1   |          1.5 | Standard-quality uncompressed WAV              |
| Spotify HiFi (Lossless)                 | FLAC       | .flac       | acodec=flac, compression_level=8, ar=44100, sample_fmt=s16   |           0.7 |          1.2 | CD-quality lossless audio                      |
| Tidal HiFi                              | FLAC       | .flac       | acodec=flac, compression_level=8, ar=44100, sample_fmt=s16   |           0.7 |          1.2 | CD-quality lossless audio                      |
| Amazon Music HD (Standard Lossless)     | FLAC       | .flac       | acodec=flac, compression_level=8, ar=44100, sample_fmt=s16   |           0.7 |          1.2 | Standard lossless streaming                    |
| Qobuz Studio (CD Quality)               | FLAC       | .flac       | acodec=flac, compression_level=8, ar=44100, sample_fmt=s16   |           0.7 |          1.2 | CD-quality lossless streaming                  |
| Deezer HiFi                             | FLAC       | .flac       | acodec=flac, compression_level=8, ar=44100, sample_fmt=s16   |           0.7 |          1.2 | CD-quality lossless streaming                  |
| Napster HiFi                            | FLAC       | .flac       | acodec=flac, compression_level=8, ar=44100, sample_fmt=s16   |           0.7 |          1.2 | CD-quality lossless streaming                  |
| YouTube Music Premium (High Quality)    | Opus       | .opus       | acodec=libopus, b:a=160k, ar=48000                           |           0.4 |          0.7 | High-efficiency lossy streaming                |
| Apple Music (Hi-Res Lossless)           | ALAC       | .m4a        | acodec=alac, ar=192000, sample_fmt=s32                       |           2.5 |          2.7 | Hi-Res lossless, ultra-high fidelity           |
| Amazon Music Ultra HD (Hi-Res Lossless) | FLAC       | .flac       | acodec=flac, compression_level=12, ar=192000, sample_fmt=s32 |           2.5 |          2.8 | Hi-Res lossless streaming                      |
| Qobuz Sublime (Hi-Res)                  | FLAC       | .flac       | acodec=flac, compression_level=12, ar=192000, sample_fmt=s32 |           2.5 |          2.8 | Hi-Res lossless audio                          |
| Tidal Master (MQA)                      | FLAC (MQA) | .flac       | acodec=flac, compression_level=12, ar=96000, sample_fmt=s32  |           1.8 |          2.3 | High-resolution MQA audio (requires unfolding) |
| FLAC Uncompressed 24bit 192kHz          | FLAC       | .flac       | acodec=flac, compression_level=0, ar=192000, sample_fmt=s32  |           3   |          3.5 | Uncompressed, ultra-high quality FLAC          |

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