import pytest
from unittest.mock import patch, MagicMock
from encoder import Encoder, EncodingError

@pytest.fixture
def encoder():
    with patch("encoder.ProfileDataManager") as mock_profile_manager, patch("encoder.ffmpeg"):
        mock_logger = MagicMock()
        mock_profile = MagicMock()
        mock_profile.Extension = ".mp3"
        mock_profile_manager.return_value.load_profiles.return_value.get_profile_by_name.return_value = mock_profile
        
        return Encoder(profile_name="test_profile", log=mock_logger)

def test_generate_unique_output_file_path(encoder):
    with patch("encoder.os.path.isfile", return_value=True), patch("encoder.os.path.exists", return_value=False):
        file_path = "test_audio.wav"
        expected_output = "test_audio.mp3"
        output = encoder._generate_unique_output_file_path(file_path, ".mp3")
        assert output == expected_output

def test_reencode_success(encoder):
    with patch("encoder.os.remove"), patch("encoder.ffmpeg.input") as mock_input, \
         patch("encoder.Stats") as mock_stats:
        mock_input.return_value.output.return_value.global_args.return_value.run.return_value = None
        input_file = "test.wav"
        output_file = "test.mp3"
        
        # Mock os.path.isfile and os.path.exists for _generate_unique_output_file_path
        with patch("encoder.os.path.isfile", return_value=True), \
             patch("encoder.os.path.exists", return_value=False):
            result = encoder.reencode(input_file, output_path=output_file)
            assert result == output_file
            encoder.logger.info.assert_called_with(f"Successfully re-encoded: {output_file}")

def test_reencode_failure(encoder):
    with patch("encoder.os.remove"), patch("encoder.ffmpeg.input") as mock_input:
        mock_input.return_value.output.return_value.global_args.return_value.run.side_effect = Exception("FFmpeg error")
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
    with patch("encoder.ffmpeg.probe", side_effect=Exception("Probe error")):
        with pytest.raises(Exception):
            encoder.get_metadata("test.wav")
        encoder.logger.error.assert_called()
