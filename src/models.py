from typing import Dict
from dataclasses import dataclass

@dataclass(frozen=True)
class Profile:
    Profile: str
    Codec: str
    Extension: str
    FFmpegSetup: Dict[str, str]
    SizeFactor: float
    CpuFactor: float
    Description: str

@dataclass(frozen=True)
class Profiles:
    profiles: Dict[str, Profile]  # Dictionary of profiles, keyed by profile name

class ProfileConstants:
    MP3_STANDARD_320KBPS = "MP3 Standard 320kbps"
    APPLE_MUSIC_LOSSLESS = "Apple Music (Lossless)"
    WAV_24BIT_44_1KHZ = "WAV (24-bit, 44.1 kHz)"
    SPOTIFY_HIFI_LOSSLESS = "Spotify HiFi (Lossless)"
    TIDAL_HIFI = "Tidal HiFi"
    AMAZON_MUSIC_HD = "Amazon Music HD (Standard Lossless)"
    QOBUZ_STUDIO = "Qobuz Studio (CD Quality)"
    DEEZER_HIFI = "Deezer HiFi"
    NAPSTER_HIFI = "Napster HiFi"
    YOUTUBE_MUSIC_PREMIUM = "YouTube Music Premium (High Quality)"
    APPLE_MUSIC_HIRES_LOSSLESS = "Apple Music (Hi-Res Lossless)"
    AMAZON_MUSIC_ULTRA_HD = "Amazon Music Ultra HD (Hi-Res Lossless)"
    QOBUZ_SUBLIME = "Qobuz Sublime (Hi-Res)"
    TIDAL_MASTER_MQA = "Tidal Master (MQA)"
    FLAC_UNCOMPRESSED_24BIT_192KHZ = "FLAC Uncompressed 24bit 192kHz"    