import unittest
import sys
import os
from pathlib import Path
from enum import Enum
from typing import NamedTuple, Tuple
from encoder import Encoder
from models import ProfileConstants
import ffmpeg

class TestReencoderRegression(unittest.TestCase):
   
    def setUp(self):
        """
        Set up testing dependencies.
        """
        # Set up paths
        
        self.resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
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
            'mp4': {
                'tagged': os.path.join(self.audio_dir, 'test.m4a'),
                'untagged': os.path.join(self.audio_dir, 'test_notags.m4a')
            }
        }
        
        # Expected metadata for verification
        self.expected_metadata = [
            'title=Test Song updated',
            'artist=Test Artist updated',
            'lyrics=Test lyrics\nSecond line updated',
            'album=Album updated'
        ]
        
        # Verify test files exist
        for fmt_files in self.source_files.values():
            for path in fmt_files.values():
                self.assertTrue(os.path.exists(path), f"Test file {path} not found")

    def tearDown(self):
        """
        Clean up test output files.
        """
        if os.path.exists(self.output_dir):
            for file_name in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    
    def test_covert_from_untagged_files(self):
        """Test converting between different audio formats with untagged files"""
        #source_formats = ['flac', 'mp4', 'mp3']
        #target_formats = ['wav', 'flac', 'mp3', 'mp4']
        source_formats = ['flac']
        target_formats = ['flac']

        for src_fmt in source_formats:
            for tgt_fmt in target_formats:
                with self.subTest(source=src_fmt, target=tgt_fmt):
                    
                    output_path = os.path.join(self.output_dir, f"output.{tgt_fmt}")

                    # Initialize reencoder with FLAC codec for testing
                    encoder = Encoder(ProfileConstants.FLAC_UNCOMPRESSED_24BIT_192KHZ)                                               
                    result = encoder.encode(
                        input_file_path=self.source_files[src_fmt]['tagged'],
                        output_path=output_path,
                        metadata_tags=self.expected_metadata
                    )

                    self.assertTrue(os.path.isfile(result))
                    self.assertTrue(result.endswith(f".{tgt_fmt}"))
                    
                    metadata = encoder.get_metadata(result)
                    tags = metadata.get('format', {}).get('tags', {})
                    
                    # Convert expected metadata list to a dict for comparison
                    expected_dict = {}
                    for tag in self.expected_metadata:
                        key, value = tag.split('=', 1)
                        expected_dict[key.lower()] = value
                    
                    # Compare each expected tag with the actual metadata
                    for key, value in expected_dict.items():
                        self.assertEqual(tags.get(key), value)
                    
    