
# Media encoder: 

## Description
Profiles:

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

## Installation
Enter the installation instructions: 

## Usage
GNU GENERAL PUBLIC LICENSE

## License
Enter the license information: 
    