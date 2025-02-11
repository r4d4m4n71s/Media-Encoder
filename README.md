# Media Encoder

A media encoding tool supporting various audio formats and streaming service profiles.

## Description

Media Encoder is a Python-based tool designed to media encoding tasks like adding metadata and encoding.

## Features

- Copy metadata to file from a json dic.
- Audio format conversion with multiple codec support (MP3, FLAC, ALAC, WAV, Opus)
- Streaming service profile support for major platforms (Spotify, Apple Music, Tidal, etc.)
- JSON-based configuration for encoding profiles
- Command-line interface for easy automation
- Standalone encoder executable
- Detailed profile information including size and CPU usage factors
- Cross-platform support

## Encoding Profiles

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


## Installation Guide

## End User Installation

For regular users who want to use the Media Encoder:

```bash
pip install media-encoder 
```

This will:
- Install required dependencies
- Verify the installation is complete

## Developer Installation

For developers who want to contribute to the Media Encoder:

```bash
# Install the package in development mode with extra dev dependencies and test
pip install media-encoder -e
```

This will:
- Install dev required dependencies including development tools
- Install the package in editable mode for development
- Verify the installation is complete

### Command Line Interface
After installation, you can use the tool from the command line:


Basic usage:
```bash
# For encoding ... overwriting same file
media-encoder input.flac "Apple Music (Lossless)"

# For encoding ... setting out ouput file
media-encoder input.flac output.mp3 "MP3 Standard 320kbps"

# For metadata adding ...

# Encoding profiles information ...
media-encoder --list-profiles
```

## Requirements

### Core Dependencies
- Python 3.8 or higher
- loguru==0.7.3 - For logging functionality
- ffmpeg for metadata copying and media processing

### Dependencies
- tabulate==0.9.0 - for presentation
- loguru==0.7.3 - for logging
- ffmpeg-python==0.2.0 - for media processing
- mutagen==1.47.0 - for metadata updating
- deepdiff==8.2.0 - for media comparison

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

### Key Points:
- Free to use, modify, and distribute
- Must keep source code open source
- Changes must be documented
- Include original license and copyright notices
- No warranty provided

For more details, visit: https://www.gnu.org/licenses/gpl-3.0.html