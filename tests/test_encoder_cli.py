import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Mock imports that might be problematic during testing if not available
# or if they have external dependencies
try:
    from models import ProfileConstants  # Replace with your actual module
except ImportError:
    ProfileConstants = MagicMock()  # Replace with a mock or dummy class

try:
    from config import FFMPEG_PATH, FFMPEG_PROFILES_PATH  # Replace with your actual module
except ImportError:
    FFMPEG_PATH = "dummy_ffmpeg_path"
    FFMPEG_PROFILES_PATH = "dummy_profiles_path"

try:
    from encoder import Encoder  # Replace with your actual module
except ImportError:
    class Encoder:  # Dummy encoder class
        def __init__(self, profile):
            self.profile = profile
        def encode(self, input_file, output_file, metadata_tags=None):
            print("Encoding")
        def copy(self, input_file, output_file, metadata_tags=None):
            print("Copying")

try:
    from data_manager import ProfileDataManager  # Replace with your actual module
except ImportError:
    class ProfileDataManager:  # Dummy class
        def load_profiles(self, profiles_path):
            return self  # Dummy return
        def __str__(self):
            return "Dummy Profile Data"

try:
    from gui.__init__ import create_audio_profiles_table  # Replace with your actual module
except ImportError:
    def create_audio_profiles_table(data_manager):  # Dummy table creation
        return "Dummy Table"


# Import the script itself AFTER mocking, to prevent early imports of those mocked modules.
from gui.encoder_cli import check_ffmpeg, show_profiles, encode, copy, kvp_as_dic, main  # Assuming your script is named program.py

# Mock global variables/constants if needed
TEST_FFMPEG_PATH = "test_ffmpeg_path"
TEST_PROFILES_PATH = "test_profiles_path"

# Fixture for capturing stdout
@pytest.fixture
def capsys(capsys):
    return capsys

# Fixtures for patching environment variables
@pytest.fixture
def mock_ffmpeg_path(monkeypatch):
    monkeypatch.setattr('gui.encoder_cli.FFMPEG_PATH', TEST_FFMPEG_PATH)
    return TEST_FFMPEG_PATH

@pytest.fixture
def mock_ffmpeg_profiles_path(monkeypatch):
    monkeypatch.setattr('gui.encoder_cli.FFMPEG_PROFILES_PATH', TEST_PROFILES_PATH)
    return TEST_PROFILES_PATH


# Unit Tests

def test_check_ffmpeg_found(mock_ffmpeg_path, monkeypatch):
    monkeypatch.setattr(os.path, 'exists', lambda path: path == TEST_FFMPEG_PATH)
    monkeypatch.setattr(os.path, 'isfile', lambda path: path == TEST_FFMPEG_PATH)
    is_installed, message = check_ffmpeg()
    assert is_installed is True
    assert "FFmpeg found" in message

def test_check_ffmpeg_not_a_file(mock_ffmpeg_path, monkeypatch):
    monkeypatch.setattr(os.path, 'exists', lambda path: path == TEST_FFMPEG_PATH)
    monkeypatch.setattr(os.path, 'isfile', lambda path: False)
    is_installed, message = check_ffmpeg()
    assert is_installed is False
    assert "FFmpeg not found" in message

def test_check_ffmpeg_not_found(mock_ffmpeg_path, monkeypatch):
    monkeypatch.setattr(os.path, 'exists', lambda path: False)
    is_installed, message = check_ffmpeg()
    assert is_installed is False
    assert "FFmpeg not found" in message

@patch('gui.encoder_cli.ProfileDataManager')
@patch('gui.encoder_cli.create_audio_profiles_table')
def test_show_profiles(mock_create_audio_profiles_table, mock_profile_data_manager, mock_ffmpeg_profiles_path, capsys):
    mock_create_audio_profiles_table.return_value = "Test Profile Table"
    mock_profile_data_manager_instance = mock_profile_data_manager.return_value
    mock_profile_data_manager_instance.load_profiles.return_value = mock_profile_data_manager_instance

    show_profiles()

    captured = capsys.readouterr()
    assert "Test Profile Table" in captured.out

@patch('gui.encoder_cli.Encoder')
def test_encode(mock_encoder, capsys):
    mock_encoder_instance = mock_encoder.return_value
    encode("input.mp3", "output.mp3", "profileA", 'key1=value1')
    mock_encoder.assert_called_once_with("profileA")
    mock_encoder_instance.encode.assert_called_once_with("input.mp3", "output.mp3", metadata_tags={"key1": "value1"})
    captured = capsys.readouterr()
    assert "Encoding complete!" in captured.out

@patch('gui.encoder_cli.Encoder')
def test_copy(mock_encoder, capsys):
    mock_encoder_instance = mock_encoder.return_value
    copy("input.mp3", "output.mp3", "key1=value1,key2=value2")
    mock_encoder_instance.copy.assert_called_once()
    captured = capsys.readouterr()
    assert "Copying complete!" in captured.out


def test_kvp_as_dic_valid():
    metadata_str = "key1=value1,key2=value2"
    expected_dict = {"key1": "value1", "key2": "value2"}
    assert kvp_as_dic(metadata_str) == expected_dict

def test_kvp_as_dic_empty():
    assert kvp_as_dic("") == {}

def test_kvp_as_dic_invalid():
    metadata_str = "key1=value1,invalid_item"
    with pytest.raises(ValueError) as excinfo:
        kvp_as_dic(metadata_str)
    assert "Invalid metadata item: invalid_item" in str(excinfo.value)


# Integration tests using main function - covering different command-line scenarios

def test_main_no_args(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with patch('sys.argv', ['program.py']):
            with patch('argparse.ArgumentParser.print_help') as mock_print_help:
                main()
        assert pytest_wrapped_e.type is SystemExit
        assert pytest_wrapped_e.value.code == 1
        captured = capsys.readouterr()
        assert "usage: program.py" in mock_print_help.call_args[0][0]

def test_main_input_no_operation(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with patch.object(sys, 'argv', ['program.py', 'input.mp3']):
            main()
    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Requires Operation (-o)." in captured.err

def test_main_encode_missing_profile(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with patch('sys.argv', ['program.py', 'input.mp3', '-o', 'encode']):
            captured = capsys.readouterr()
            main()
    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Profile is required" in captured.err

@patch('gui.encoder_cli.encode')
def test_main_encode_success(mock_encode, capsys):
    with patch('sys.argv', ['program.py', 'input.mp3', 'output.mp3', '-o', 'encode', '-p', 'profileA']):
        main()
    mock_encode.assert_called_once_with('input.mp3', 'output.mp3', 'profileA', None)
    captured = capsys.readouterr()

@patch('gui.encoder_cli.copy')
def test_main_copy_success(mock_copy, capsys):
    with patch('sys.argv', ['program.py', 'input.mp3', 'output.mp3', '-o', 'copy', '-m', 'key1=value1']):
        main()
    mock_copy.assert_called_once_with('input.mp3', 'output.mp3', 'key1=value1')
    captured = capsys.readouterr()

@patch('sys.exit')
def test_main_show_profiles(mock_exit, capsys):
    with patch('sys.argv', ['program.py', '-p']):
        with patch('gui.encoder_cli.show_profiles') as mock_show_profiles:
            main()
            mock_show_profiles.assert_called_once()
            captured = capsys.readouterr()
            assert "Choose profile below." in captured.out

def test_main_input_output(capsys):
    with patch('sys.argv', ['program.py', 'input.mp3', 'output.mp3']):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            main()
        assert pytest_wrapped_e.type is SystemExit
        assert pytest_wrapped_e.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Requires Operation (-o)." in captured.err