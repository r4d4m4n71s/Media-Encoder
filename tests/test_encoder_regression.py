import unittest
import os
from encoder import Encoder
from data_manager import ProfileDataManager
from config import FFMPEG_PROFILES_PATH, logger

class TestReencoderRegression(unittest.TestCase):
   
    def setUp(self):
        """
        Set up testing dependencies.
        """
        # Set up paths
        
        self.resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        self.dataManater = ProfileDataManager().load_profiles(FFMPEG_PROFILES_PATH)
        
        self.logger = logger.bind(name="test_logger")
        self.logger.add(os.path.join(self.output_dir ,"test.log"), rotation="5 MB", level="DEBUG", format="{time} {level} {message}", enqueue=True, mode='w')
                 
        os.makedirs(self.output_dir, exist_ok=True)
                
        # Source files for tests (both with and without tags)
        self.audio_dir = os.path.join(self.resources_dir, 'audio')
        self.source_files = {
            'wav': {
                'tagged': os.path.join(self.audio_dir, 'test.wav'),
                'untagged': os.path.join(self.audio_dir, 'test_notags.wav')
            },
            'flac': {
                'tagged': os.path.join(self.audio_dir, 'test.flac'),
                'untagged': os.path.join(self.audio_dir, 'test_notags.flac')
            },
            'mp3': {
                'tagged': os.path.join(self.audio_dir, 'test.mp3'),
                'untagged': os.path.join(self.audio_dir, 'test_notags.mp3')
            },
            'm4a': {
                'tagged': os.path.join(self.audio_dir, 'test.m4a'),
                'untagged': os.path.join(self.audio_dir, 'test_notags.m4a')
            }
        }
        
        # Expected metadata for verification
        self.expected_metadata = {
            "artist": "John Doe",
            "album": "My Album",
            "comment": "Converted using FFmpeg"
        }
        
        # Verify test files exist
        for fmt_files in self.source_files.values():
            for path in fmt_files.values():
                self.assertTrue(os.path.exists(path), f"Test file {path} not found")

    def tearDown(self):
        """
        Clean up test output files.
        """
        # Remove the file handler and close the file
        logger.remove()
        
        if os.path.exists(self.output_dir):
            for file_name in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    
    def test_copy_from_tagged_files(self):
        """Test converting between different audio formats with tagged files"""
        source_formats = ['flac', 'm4a', 'mp3']
                
        for src_fmt in source_formats:            
            with self.subTest(source=src_fmt, target=src_fmt):
                
                self.logger.info(f"Encoding from {src_fmt} ...")            
                self.logger.info(f"Encoding to {src_fmt} ...")
                profile = self.dataManater.get_profiles_by_extension(f".{src_fmt}")[0]
                self.logger.info(f"Using profile: {profile.Name} ...")
                
                input_file_path = self.source_files[src_fmt]['tagged']
                output_file_path = os.path.join(self.output_dir, f"output.{src_fmt}")
            
                # Initialize reencoder with FLAC codec for testing
                encoder = Encoder(profile.Name)                                               
                result = encoder.copy(
                    input_file_path=input_file_path,
                    output_path=output_file_path,
                    metadata_tags=self.expected_metadata
                )

                self.assertTrue(os.path.isfile(result))
                self.assertTrue(result.endswith(f".{src_fmt}"))
                
                metadata = encoder.get_metadata(result)
                tags = metadata.get('format', {}).get('tags', {})
                
                # Compare each expected tag with the actual metadata
                for key, value in self.expected_metadata.items():
                    self.assertEqual(tags.get(key.lower()), value)

    def test_covert_from_tagged_files(self):
        """Test converting between different audio formats with tagged files"""
        source_formats = ['flac', 'm4a', 'mp3']
        target_formats = ['wav', 'flac', 'mp3', 'm4a']
        #source_formats = ['m4a']
        #target_formats = ['wav']

        for src_fmt in source_formats:
            for tgt_fmt in target_formats:
                with self.subTest(source=src_fmt, target=tgt_fmt):
                    
                    self.logger.info(f"Encoding from {src_fmt} ...")            
                    self.logger.info(f"Encoding to {tgt_fmt} ...")
                    profile = self.dataManater.get_profiles_by_extension(f".{tgt_fmt}")[0]
                    self.logger.info(f"Using profile: {profile.Name} ...")
                    
                    input_file_path = self.source_files[src_fmt]['tagged']
                    output_file_path = os.path.join(self.output_dir, f"output.{tgt_fmt}")
                
                    # Initialize reencoder with FLAC codec for testing
                    encoder = Encoder(profile.Name)                                               
                    result = encoder.encode(
                        input_file_path=input_file_path,
                        output_path=output_file_path,
                        metadata_tags=self.expected_metadata
                    )

                    self.assertTrue(os.path.isfile(result))
                    self.assertTrue(result.endswith(f".{tgt_fmt}"))
                    
                    metadata = encoder.get_metadata(result)
                    tags = metadata.get('format', {}).get('tags', {})
                    
                    # Compare each expected tag with the actual metadata
                    for key, value in self.expected_metadata.items():
                        self.assertEqual(tags.get(key.lower()), value)
                    
    def test_covert_from_untagged_files(self):
        """Test converting between different audio formats with untagged files"""
        source_formats = ['flac', 'm4a', 'mp3']
        target_formats = ['wav', 'flac', 'mp3', 'm4a']
        #source_formats = ['m4a']
        #target_formats = ['wav']

        for src_fmt in source_formats:
            for tgt_fmt in target_formats:
                with self.subTest(source=src_fmt, target=tgt_fmt):
                    
                    self.logger.info(f"Encoding from {src_fmt} ...")            
                    self.logger.info(f"Encoding to {tgt_fmt} ...")
                    profile = self.dataManater.get_profiles_by_extension(f".{tgt_fmt}")[0]
                    self.logger.info(f"Using profile: {profile.Name} ...")
                    
                    input_file_path = self.source_files[src_fmt]['untagged']
                    output_file_path = os.path.join(self.output_dir, f"output.{tgt_fmt}")
                
                    # Initialize reencoder with FLAC codec for testing
                    encoder = Encoder(profile.Name)                                               
                    result = encoder.encode(
                        input_file_path=input_file_path,
                        output_path=output_file_path,
                        metadata_tags=self.expected_metadata
                    )

                    self.assertTrue(os.path.isfile(result))
                    self.assertTrue(result.endswith(f".{tgt_fmt}"))
                    
                    metadata = encoder.get_metadata(result)
                    tags = metadata.get('format', {}).get('tags', {})
                    
                    # Compare each expected tag with the actual metadata
                    for key, value in self.expected_metadata.items():
                        self.assertEqual(tags.get(key.lower()), value)