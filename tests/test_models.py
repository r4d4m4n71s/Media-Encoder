import pytest
from dataclasses import FrozenInstanceError
from src.models import Profile, Profiles, ProfileConstants

def test_profile_creation():
    """Test creating a Profile instance with valid data."""
    profile = Profile(
        Profile="Test Profile",
        Codec="mp3",
        Extension=".mp3",
        FFmpegSetup={"bitrate": "320k"},
        SizeFactor=1.0,
        CpuFactor=1.0,
        Description="Test profile description"
    )
    
    assert profile.Profile == "Test Profile"
    assert profile.Codec == "mp3"
    assert profile.Extension == ".mp3"
    assert profile.FFmpegSetup == {"bitrate": "320k"}
    assert profile.SizeFactor == 1.0
    assert profile.CpuFactor == 1.0
    assert profile.Description == "Test profile description"

def test_profile_immutability():
    """Test that Profile instances are immutable (frozen)."""
    profile = Profile(
        Profile="Test Profile",
        Codec="mp3",
        Extension=".mp3",
        FFmpegSetup={"bitrate": "320k"},
        SizeFactor=1.0,
        CpuFactor=1.0,
        Description="Test profile description"
    )
    
    with pytest.raises(FrozenInstanceError):
        profile.Profile = "New Name"

def test_profiles_container():
    """Test the Profiles container class."""
    profile1 = Profile(
        Profile="Profile 1",
        Codec="mp3",
        Extension=".mp3",
        FFmpegSetup={"bitrate": "320k"},
        SizeFactor=1.0,
        CpuFactor=1.0,
        Description="First test profile"
    )
    
    profile2 = Profile(
        Profile="Profile 2",
        Codec="flac",
        Extension=".flac",
        FFmpegSetup={"compression_level": "8"},
        SizeFactor=2.0,
        CpuFactor=1.5,
        Description="Second test profile"
    )
    
    profiles = Profiles(profiles={
        "profile1": profile1,
        "profile2": profile2
    })
    
    assert len(profiles.profiles) == 2
    assert profiles.profiles["profile1"] == profile1
    assert profiles.profiles["profile2"] == profile2

def test_profile_constants():
    """Test that ProfileConstants contains expected streaming service profiles."""
    assert ProfileConstants.MP3_STANDARD_320KBPS == "MP3 Standard 320kbps"
    assert ProfileConstants.APPLE_MUSIC_LOSSLESS == "Apple Music (Lossless)"
    assert ProfileConstants.WAV_24BIT_44_1KHZ == "WAV (24-bit, 44.1 kHz)"
    assert ProfileConstants.SPOTIFY_HIFI_LOSSLESS == "Spotify HiFi (Lossless)"
    assert ProfileConstants.TIDAL_HIFI == "Tidal HiFi"
    assert ProfileConstants.AMAZON_MUSIC_HD == "Amazon Music HD (Standard Lossless)"
    assert ProfileConstants.QOBUZ_STUDIO == "Qobuz Studio (CD Quality)"
    assert ProfileConstants.DEEZER_HIFI == "Deezer HiFi"
    assert ProfileConstants.NAPSTER_HIFI == "Napster HiFi"
    assert ProfileConstants.YOUTUBE_MUSIC_PREMIUM == "YouTube Music Premium (High Quality)"
    assert ProfileConstants.APPLE_MUSIC_HIRES_LOSSLESS == "Apple Music (Hi-Res Lossless)"
    assert ProfileConstants.AMAZON_MUSIC_ULTRA_HD == "Amazon Music Ultra HD (Hi-Res Lossless)"
    assert ProfileConstants.QOBUZ_SUBLIME == "Qobuz Sublime (Hi-Res)"
    assert ProfileConstants.TIDAL_MASTER_MQA == "Tidal Master (MQA)"
    assert ProfileConstants.FLAC_UNCOMPRESSED_24BIT_192KHZ == "FLAC Uncompressed 24bit 192kHz"