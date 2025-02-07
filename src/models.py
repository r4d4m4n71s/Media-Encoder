"""
Audio encoding profile models for the Media Encoder.

This module defines the data structures used to represent audio encoding profiles,
including their codec settings, performance characteristics, and standard streaming
service configurations.
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass(frozen=True)
class Profile:
    """
    Represents an audio encoding profile with specific codec settings and performance characteristics.
    
    The Profile class is immutable (frozen) to ensure profile consistency during encoding operations.
    Each profile contains the necessary information for FFmpeg encoding and performance estimation.
    
    Attributes:
        Profile (str): The name of the profile (e.g., "MP3 320kbps", "FLAC Lossless")
        Codec (str): The audio codec used (e.g., 'mp3', 'flac', 'wav')
        Extension (str): The file extension for this codec (e.g., '.mp3', '.flac')
        FFmpegSetup (str): FFmpeg command-line parameters for this profile
        SizeFactor (float): Relative size factor compared to original file (1.0 = same size)
        CpuFactor (float): Relative CPU usage factor for encoding (1.0 = baseline)
        Description (str): Detailed description of the profile's characteristics
    """
    Name: str
    Codec: str
    Extension: str
    FFmpegSetup: str
    SizeFactor: float
    CpuFactor: float
    Description: str

@dataclass(frozen=True)
class Argument:
    Name: str
    Default: str
    Description: str

class ProfileConstants:
    """
    Constants representing standard audio streaming service profiles and common formats.
    
    This class provides a centralized collection of profile names that match
    the specifications of major streaming services and common audio formats.
    These constants ensure consistent profile naming across the application
    and make it easier to reference specific quality targets.
    
    The profiles are organized into categories:
    - Standard formats (MP3, WAV)
    - Streaming service profiles (Spotify, Apple Music, etc.)
    - Hi-Res audio profiles
    """
    # Standard formats
    MP3_STANDARD_320KBPS = "MP3 Standard 320kbps"
    WAV_24BIT_44_1KHZ = "WAV (24-bit, 44.1 kHz)"
    FLAC_UNCOMPRESSED_24BIT_192KHZ = "FLAC Uncompressed 24bit 192kHz"
    
    # Streaming service standard quality profiles
    SPOTIFY_HIFI_LOSSLESS = "Spotify HiFi (Lossless)"
    APPLE_MUSIC_LOSSLESS = "Apple Music (Lossless)"
    TIDAL_HIFI = "Tidal HiFi"
    DEEZER_HIFI = "Deezer HiFi"
    AMAZON_MUSIC_HD = "Amazon Music HD (Standard Lossless)"
    QOBUZ_STUDIO = "Qobuz Studio (CD Quality)"
    NAPSTER_HIFI = "Napster HiFi"
    YOUTUBE_MUSIC_PREMIUM = "YouTube Music Premium (High Quality)"
    
    # Hi-Res streaming profiles
    APPLE_MUSIC_HIRES_LOSSLESS = "Apple Music (Hi-Res Lossless)"
    AMAZON_MUSIC_ULTRA_HD = "Amazon Music Ultra HD (Hi-Res Lossless)"
    QOBUZ_SUBLIME = "Qobuz Sublime (Hi-Res)"
    TIDAL_MASTER_MQA = "Tidal Master (MQA)"