import pytest
import subprocess
from unittest.mock import patch, MagicMock
from encoder import Encoder, EncodingError

@pytest.fixture
def encoder():
    with patch("encoder.ProfileDataManager") as mock_profile_manager, \
         patch("encoder.ffmpeg"):
        mock_logger = MagicMock()
        mock_profile = MagicMock()
        mock_profile.Extension = ".mp3"
        mock_profile_manager.return_value.load_profiles.return_value.get_profile_by_name.return_value = mock_profile
        mock_profile_manager.return_value.load_arguments.return_value.get_arguments_as_dict.return_value = {}
        
        return Encoder(profile="test_profile", logger=mock_logger)

def test_generate_unique_output_file_path(encoder):
    # First call returns True to simulate existing file, second call False for non-existing file
    with patch("encoder.os.path.exists", side_effect=[True, False]):
        file_path = "test_audio.wav"
        expected_output = "test_audio_Encoded.mp3"
        output = encoder._generate_unique_output_file_path(file_path, ".mp3")
        assert output == expected_output

def test_encode_success(encoder):
    with patch("encoder.os.remove"), \
         patch("encoder.os.path.isfile", return_value=True), \
         patch("encoder.Stats") as mock_stats:
        mock_stats_instance = MagicMock()
        mock_stats.return_value = mock_stats_instance
        
        # Mock FFmpegCommand methods
        mock_run = MagicMock()
        encoder.ffmpeg_cmd.run = mock_run
        
        input_file = "test.wav"
        output_file = "test.mp3"
        
        # Mock os.path.exists for _generate_unique_output_file_path
        with patch("encoder.os.path.exists", return_value=False):
            result = encoder.encode(input_file, output_path=output_file)
            assert result == output_file
            mock_stats_instance.compare_file_sizes.assert_called_once()
            mock_run.assert_called_once()

def test_encode_failure(encoder):
    with patch("encoder.os.remove"), \
         patch("encoder.os.path.isfile", return_value=True):
        # Mock FFmpegCommand methods
        mock_run = MagicMock()
        mock_run.side_effect = subprocess.CalledProcessError(1, "ffmpeg", stderr=b"FFmpeg error")
        encoder.ffmpeg_cmd.run = mock_run
        
        input_file = "test.wav"
        output_file = "test.mp3"
        
        with pytest.raises(EncodingError):
            encoder.encode(input_file, output_path=output_file)
        encoder.logger.error.assert_called()

def test_get_metadata_failure(encoder):
    with patch("encoder.ffmpeg") as mock_ffmpeg:
        # Create a real ffmpeg.Error instance
        error = type('Error', (Exception,), {'stderr': b'Error message'})()
        mock_ffmpeg.Error = error.__class__
        mock_ffmpeg.probe.side_effect = error
        
        with pytest.raises(Exception) as exc_info:
            encoder.get_metadata("test.wav")
        assert isinstance(exc_info.value, error.__class__)
        encoder.logger.error.assert_called()
