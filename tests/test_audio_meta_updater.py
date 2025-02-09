import os
import unittest
import json
import shutil
from config import MUTAGEN_AUDIO_TAGS

from meta_updater import AudioMetaUpdater, MetadataError

class TestAudioMetaUpdaterRegression(unittest.TestCase):
    def setUp(self):
        self.resources_dir = os.path.join(os.path.dirname(__file__), 'resources/audio')
        self.output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(self.output_dir, exist_ok=True)
        self.tags_path = MUTAGEN_AUDIO_TAGS
        self.cover_path = os.path.join(self.output_dir, "cover.jpg")

        self.test_files = {
            'flac': 'test.flac',
            'mp3': 'test.mp3',
            'm4a': 'test.m4a',
            'wav': 'test.wav',
            'jpg': 'cover.jpg',
            'flac_notags': 'test_notags.flac',
            'mp3_notags': 'test_notags.mp3',
            'm4a_notags': 'test_notags.m4a',
            'wav_notags': 'test_notags.wav'
        }
        self.metadata = [
            ('title', 'Test Title'),
            ('album', 'Test Album'),
            ('artist', 'Test Artist'),
            ('genre', 'Test Genre'),
            ('date', '2023-01-01'),
            ('composer', 'Test Composer'),
            ('isrc', 'TEST12345678'),
            ('lyrics', 'Test Lyrics'),
            ('cover_art', f'{self.output_dir}/cover.jpg'),
            ('copyright', '© 2023 Test Records'),
            ('discnumber', '3'),
            ('disctotal', '1'),
            ('custom_tag', 'Custom Value')
        ]

        # Create a copy of the test files in the resources directory
        for file_type, file_name in self.test_files.items():
            src = os.path.join(self.resources_dir, file_name)
            dst = os.path.join(self.output_dir, file_name)
            shutil.copyfile(src, dst)

    def tearDown(self):
        # Remove copied test files
        for file_name in self.test_files.values():
            if os.path.exists(os.path.join(self.output_dir, file_name)):
                os.remove(os.path.join(self.output_dir, file_name))

    def test_update_flac_metadata(self):
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
        original_tags = updater.get_current_tags()
        updater.update_metadata_list(self.metadata, encoding=3, lang='eng')
        updated_tags = updater.get_current_tags()
        diff = updater.get_metadata_diff(original_tags, updated_tags)
        self.assertNotEqual(diff, {})
        with open(os.path.join(self.output_dir, self.test_files['flac'])+".json", "w") as json_file:
            json_file.write(diff)

    def test_update_mp3_metadata(self):
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['mp3']), self.tags_path)
        original_tags = updater.get_current_tags()
        updater.update_metadata_list(self.metadata, encoding=3, lang='eng')
        updated_tags = updater.get_current_tags()
        diff = updater.get_metadata_diff(original_tags, updated_tags)
        self.assertNotEqual(diff, {})
        with open(os.path.join(self.output_dir, self.test_files['mp3'])+".json", "w") as json_file:
            json_file.write(diff)

    def test_update_wave_metadata(self):
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['wav']), self.tags_path)
        original_tags = updater.get_current_tags()
        updater.update_metadata_list(self.metadata, encoding=3, lang='eng')
        updated_tags = updater.get_current_tags()
        diff = updater.get_metadata_diff(original_tags, updated_tags)
        self.assertNotEqual(diff, {})

    def test_update_m4a_metadata(self):
        """Test updating M4A metadata."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['m4a']), self.tags_path)
        original_tags = updater.get_current_tags()
        updater.update_metadata_list(self.metadata, encoding=3, lang='eng')
        updated_tags = updater.get_current_tags()
        diff = updater.get_metadata_diff(original_tags, updated_tags)
        self.assertNotEqual(diff, {})
        with open(os.path.join(self.output_dir, self.test_files['m4a'])+".json", "w") as json_file:
            json_file.write(diff)

    def test_invalid_encoding_value(self):
        """Test validation of encoding parameter."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
        with self.assertRaises(ValueError) as context:
            updater.update_metadata_list(self.metadata, encoding=0, lang='eng')
        self.assertIn("must be between 1 and 4", str(context.exception))

        with self.assertRaises(ValueError) as context:
            updater.update_metadata_list(self.metadata, encoding=5, lang='eng')
        self.assertIn("must be between 1 and 4", str(context.exception))

    def test_invalid_language_code(self):
        """Test validation of language code parameter."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
        with self.assertRaises(ValueError) as context:
            updater.update_metadata_list(self.metadata, encoding=3, lang='en')  # 2 chars
        self.assertIn("must be a 3-letter ISO 639-2 code", str(context.exception))

        with self.assertRaises(ValueError) as context:
            updater.update_metadata_list(self.metadata, encoding=3, lang='engl')  # 4 chars
        self.assertIn("must be a 3-letter ISO 639-2 code", str(context.exception))

    def test_unsupported_image_format(self):
        """Test handling of unsupported image formats for cover art."""
        metadata_with_bmp = [('cover_art', os.path.join(self.output_dir, 'test.bmp'))]
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
        
        # Create a temporary BMP file
        with open(os.path.join(self.output_dir, 'test.bmp'), 'wb') as f:
            f.write(b'BMP')
        
        try:
            with self.assertRaises(MetadataError) as context:
                updater.update_metadata_list(metadata_with_bmp)
            self.assertIn("Unsupported image format", str(context.exception))
        finally:
            # Clean up
            if os.path.exists(os.path.join(self.output_dir, 'test.bmp')):
                os.remove(os.path.join(self.output_dir, 'test.bmp'))

    def test_missing_cover_art(self):
        """Test handling of missing cover art files."""
        metadata_with_missing = [('cover_art', 'nonexistent.jpg')]
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
        
        with self.assertRaises(FileNotFoundError) as context:
            updater.update_metadata_list(metadata_with_missing)
        self.assertIn("Cover art file not found", str(context.exception))

    def test_invalid_metadata_values(self):
        """Test handling of invalid metadata values."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
        
        # Test with complex object that can't be converted to string
        invalid_metadata = [('title', {'complex': 'object'})]
        with self.assertRaises(ValueError) as context:
            updater.update_metadata_list(invalid_metadata)
        self.assertIn("Invalid value type", str(context.exception))

        # Test with empty string value
        empty_metadata = [('title', '   ')]
        updater.update_metadata_list(empty_metadata)  # Should skip empty values
        self.assertNotIn('title', updater.get_current_tags())

    def test_update_metadata_from_json_success(self):
        """Test successful metadata update from JSON file."""
        json_metadata = [
            {'tag_key': 'title', 'value': 'JSON Title'},
            {'tag_key': 'album', 'value': 'JSON Album'},
            {'tag_key': 'artist', 'value': 'JSON Artist'},
            {'tag_key': 'genre', 'value': 'JSON Genre'},
            {'tag_key': 'date', 'value': '2023-01-01'},
            {'tag_key': 'composer', 'value': 'JSON Composer'},
            {'tag_key': 'isrc', 'value': 'JSON12345678'},
            {'tag_key': 'lyrics', 'value': 'JSON Lyrics'},
            {'tag_key': 'cover_art', 'value': f'{self.output_dir}/cover.jpg'},
            {'tag_key': 'copyright', 'value': '© 2023 JSON Records'},
            {'tag_key': 'discnumber', 'value': '3'},
            {'tag_key': 'disctotal', 'value': '1'},
            {'tag_key': 'custom_tag', 'value': 'Custom JSON Value'}
        ]
        json_file = os.path.join(self.output_dir, 'metadata.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_metadata, f)

        try:
            updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
            original_tags = updater.get_current_tags()
            updater.update_metadata_from_json(json_file)
            updated_tags = updater.get_current_tags()
            diff = updater.get_metadata_diff(original_tags, updated_tags)
            self.assertNotEqual(diff, {})
        finally:
            if os.path.exists(json_file):
                os.remove(json_file)

    def test_update_metadata_from_invalid_json(self):
        """Test handling of invalid JSON metadata files."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
        
        # Test with invalid JSON format
        invalid_json = os.path.join(self.output_dir, 'invalid.json')
        with open(invalid_json, 'w') as f:
            f.write('{"invalid json')
        
        try:
            with self.assertRaises(MetadataError) as context:
                updater.update_metadata_from_json(invalid_json)
            self.assertIn("Invalid JSON format", str(context.exception))
        finally:
            if os.path.exists(invalid_json):
                os.remove(invalid_json)

        # Test with wrong structure (not a list)
        wrong_structure = os.path.join(self.output_dir, 'wrong_structure.json')
        with open(wrong_structure, 'w') as f:
            json.dump({'not': 'a list'}, f)
        
        try:
            with self.assertRaises(ValueError) as context:
                updater.update_metadata_from_json(wrong_structure)
            self.assertIn("must contain a list", str(context.exception))
        finally:
            if os.path.exists(wrong_structure):
                os.remove(wrong_structure)

        # Test with missing required fields
        missing_fields = os.path.join(self.output_dir, 'missing_fields.json')
        with open(missing_fields, 'w') as f:
            json.dump([{'wrong_key': 'value'}], f)
        
        try:
            with self.assertRaises(ValueError) as context:
                updater.update_metadata_from_json(missing_fields)
            self.assertIn("must have 'tag_key' and 'value' fields", str(context.exception))
        finally:
            if os.path.exists(missing_fields):
                os.remove(missing_fields)

    def test_nonexistent_json_file(self):
        """Test handling of nonexistent JSON files."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac']), self.tags_path)
        with self.assertRaises(FileNotFoundError) as context:
            updater.update_metadata_from_json('nonexistent.json')
        self.assertIn("Metadata JSON file not found", str(context.exception))

    def test_update_flac_notags_metadata(self):
        """Test updating metadata for FLAC file without existing tags."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['flac_notags']), self.tags_path)
        original_tags = updater.get_current_tags()
        self.assertEqual(len(original_tags), 1, "File should have only a initial tag")
        updater.update_metadata_list(self.metadata, encoding=3, lang='eng')
        updated_tags = updater.get_current_tags()
        diff = updater.get_metadata_diff(original_tags, updated_tags)
        self.assertNotEqual(diff, {})
        with open(os.path.join(self.output_dir, self.test_files['flac_notags'])+".json", "w") as json_file:
            json_file.write(diff)

    def test_update_mp3_notags_metadata(self):
        """Test updating metadata for MP3 file without existing tags."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['mp3_notags']), self.tags_path)
        original_tags = updater.get_current_tags()
        self.assertEqual(len(original_tags), 1, "File should have only a initial tag")
        updater.update_metadata_list(self.metadata, encoding=3, lang='eng')
        updated_tags = updater.get_current_tags()
        diff = updater.get_metadata_diff(original_tags, updated_tags)
        self.assertNotEqual(diff, {})
        with open(os.path.join(self.output_dir, self.test_files['mp3_notags'])+".json", "w") as json_file:
            json_file.write(diff)

    def test_update_m4a_notags_metadata(self):
        """Test updating metadata for M4A file without existing tags."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['m4a_notags']), self.tags_path)
        original_tags = updater.get_current_tags()
        self.assertEqual(len(original_tags), 1, "File should have only a initial tag")
        updater.update_metadata_list(self.metadata, encoding=3, lang='eng')
        updated_tags = updater.get_current_tags()
        diff = updater.get_metadata_diff(original_tags, updated_tags)
        self.assertNotEqual(diff, {})
        with open(os.path.join(self.output_dir, self.test_files['m4a_notags'])+".json", "w") as json_file:
            json_file.write(diff)

    def test_update_wave_notags_metadata(self):
        """Test updating metadata for WAV file without existing tags."""
        updater = AudioMetaUpdater(os.path.join(self.output_dir, self.test_files['wav_notags']), self.tags_path)
        original_tags = updater.get_current_tags()
        self.assertEqual(original_tags, {}, "File should have no initial tags")
        updater.update_metadata_list(self.metadata, encoding=3, lang='eng')
        updated_tags = updater.get_current_tags()
        diff = updater.get_metadata_diff(original_tags, updated_tags)
        self.assertNotEqual(diff, {})
        with open(os.path.join(self.output_dir, self.test_files['wav_notags'])+".json", "w") as json_file:
            json_file.write(diff)