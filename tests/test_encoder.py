import pytest
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
        
        return Encoder(profile_name="test_profile", logger=mock_logger)

def test_generate_unique_output_file_path(encoder):
    # First call returns True to simulate existing file, second call False for non-existing file
    with patch("encoder.os.path.exists", side_effect=[True, False]):
        file_path = "test_audio.wav"
        expected_output = "test_audio_Encoded.mp3"
        output = encoder._generate_unique_output_file_path(file_path, ".mp3")
        assert output == expected_output

def test_reencode_success(encoder):
    with patch("encoder.os.remove"), \
         patch("encoder.os.path.isfile", return_value=True), \
         patch("encoder.ffmpeg.input") as mock_input, \
         patch("encoder.Stats") as mock_stats:
        mock_input.return_value.output.return_value.global_args.return_value.run.return_value = None
        mock_stats_instance = MagicMock()
        mock_stats.return_value = mock_stats_instance
        
        input_file = "test.wav"
        output_file = "test.mp3"
        
        # Mock os.path.exists for _generate_unique_output_file_path
        with patch("encoder.os.path.exists", return_value=False):
            result = encoder.reencode(input_file, output_path=output_file)
            assert result == output_file
            encoder.logger.success.assert_called_with(f"Successfully re-encoded: {output_file}")
            mock_stats_instance.compare_file_sizes.assert_called_once()

def test_reencode_failure(encoder):
    with patch("encoder.os.remove"), \
         patch("encoder.os.path.isfile", return_value=True), \
         patch("encoder.ffmpeg.input") as mock_input, \
         patch("encoder.ffmpeg.Error", Exception, create=True):  # Mock ffmpeg.Error as Exception
        error = Exception("FFmpeg error")
        error.stderr = b"FFmpeg error details"
        mock_input.return_value.output.return_value.global_args.return_value.run.side_effect = error
        input_file = "test.wav"
        output_file = "test.mp3"
        
        with pytest.raises(EncodingError):
            encoder.reencode(input_file, output_path=output_file)
        encoder.logger.error.assert_called()

def test_map_metadata(encoder):
    tags = ["artist=Test Artist", "album=Test Album"]
    expected_output = {'-metadata:artist': 'Test Artist', '-metadata:album': 'Test Album'}
    result = encoder._map_metadata(tags)
    assert result == expected_output

def test_get_metadata_failure(encoder):
    with patch("encoder.ffmpeg") as mock_ffmpeg, \
         patch("encoder.ffmpeg.Error", Exception, create=True):  # Mock ffmpeg.Error as Exception
        error = Exception("Probe error")
        error.stderr = b"Error message"
        mock_ffmpeg.probe.side_effect = error
        
        with pytest.raises(Exception):
            encoder.get_metadata("test.wav")
        encoder.logger.error.assert_called()
