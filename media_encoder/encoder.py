import ffmpeg
import subprocess
import os
from typing import Dict, Optional
from loguru import logger
from data_manager import ProfileDataManager, Profile
from config import FFMPEG_PROFILES_PATH, FFMPEG_GLOBALARGS_PATH, FFMPEG_PATH, FFPROBE_PATH, get_logger

class EncodingError(Exception):
    """Custom exception for processing errors."""
    pass

class Encoder:
    """
    A class to handle encoding and metadata manipulation using FFmpeg.
    """
    def __init__(self, profile, logger: logger = None): # type: ignore
        """
        Initialize the Reencoder with the codec configuration.

        Args:
            codec: Codec configuration for re-encoding.
            logger: Optional logger instance. If not provided, creates a new one.           

        Raises:
            ValueError: If codec is None or invalid.
        """
        if isinstance(profile, str):
            self.profile = ProfileDataManager().load_profiles(FFMPEG_PROFILES_PATH).get_profile_by_name(profile)  
        elif isinstance(profile, Profile):
            self.profile = profile

        self.logger = logger if logger is not None else get_logger(__name__)        
        self.ffmpeg_cmd = FFmpegCommand(FFMPEG_PATH)
    
    # Use ffmpeg-python to copy streams without re-encoding
    def copy(
        self,
        input_file_path: str,
        output_path: Optional[str] = None,
        delete_original: bool = False,
        metadata_tags: Optional[Dict[str, str]] = None,
        ffmpeg_output_args: Optional[Dict[str, str]] = None,
        ffmpeg_global_args: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        self.logger.info("Copying...")

        if ffmpeg_output_args:
            ffmpeg_output_args.update({'c':'copy'})
        else:    
            ffmpeg_output_args = {'c':'copy'}
            
        return self.encode(input_file_path, output_path, delete_original, metadata_tags, ffmpeg_output_args, ffmpeg_global_args)

    def encode(
        self,
        input_file_path: str,
        output_path: Optional[str] = None,
        delete_original: bool = False,
        metadata_tags: Optional[Dict[str, str]] = None,
        ffmpeg_output_args: Optional[Dict[str, str]] = None,
        ffmpeg_global_args: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        Re-encode the file to the specified codec and optionally modify metadata.

        Args:
            input_file_path: Path to the input file
            output_path: Optional path for the output file
            delete_original: Whether to delete the original file after encoding
            metadata_tags: List of metadata tags to modify (format: "key=value")
            ffmpeg_output_args: Additional FFmpeg output args
            ffmpeg_global_args: Additional FFmpeg global args

        Returns:
            Path to the output file if successful, None otherwise

        Raises:
            EncodingError: If encoding fails
        """        
        if not os.path.isfile(input_file_path):
            raise ValueError(f"File does not exist: {input_file_path}")
        
        output_file_path = self._generate_unique_output_file_path(output_path or input_file_path, self.profile.Extension)
        
        try:            
            # add default output args
            output_args: dict[str,str] = ProfileDataManager.get_FFmpegSetup_as_dict(self.profile)
                                                                 
            # add user output args
            output_args.update(ffmpeg_output_args or {})
            
            # add default global args
            global_args: dict[str,str] = ProfileDataManager().load_arguments(FFMPEG_GLOBALARGS_PATH).get_arguments_as_dict()      

            # add user global args
            global_args.update(ffmpeg_global_args or {})                        
            
            # format global args
            global_args_formated = self._format_global_args(global_args)
            
            # Create the FFmpeg command
            ffmpeg_command = self.ffmpeg_cmd.input(input_file_path).output(output_file_path)
            
            ffmpeg_command = ffmpeg_command.global_args(global_args_formated)
            ffmpeg_command = ffmpeg_command.output_args(output_args)
            if metadata_tags:
                ffmpeg_command = ffmpeg_command.metadata(metadata_tags)
                                    
            ffmpeg_command.run(capture_stdout=True, capture_stderr=True)
            
            # check the stats
            Stats(input_file_path, output_file_path).compare_file_sizes()

            # Optionally delete the original file
            if delete_original and input_file_path != output_path:
                try:
                    os.remove(input_file_path)
                    self.logger.debug(f"Deleted original file: {input_file_path}")
                except OSError as e:
                    self.logger.warning(f"Failed to delete original file {input_file_path}: {str(e)}")

        except OSError as e:
            # Handle file system related errors
            error_msg = str(e)
            self.logger.error(f"File system error during re-encoding of {input_file_path}: {error_msg}")
            raise EncodingError(f"File system error re-encoding {input_file_path}: {error_msg}") from e
        except Exception as e:
            # Handle any other unexpected errors
            error_msg = str(e)
            self.logger.error(f"Unexpected error during re-encoding: {input_file_path}: {error_msg}")
            raise EncodingError(f"Unexpected error re-encoding {input_file_path}: {error_msg}") from e

        return output_file_path
    
    def _format_global_args(self, global_args:dict[str, str]) -> list[str]:         
        # Replace empty or null values 
        result = []
        for key, value in global_args.items():
            if key.startswith('-') and key.strip():  # Only include keys that start with '-'
                result.append(key)
            if value is not None and str(value).strip():
                result.append(str(value))
        return result
    
    def _generate_unique_output_file_path(self, file_path, extension: str, rename='Encoded') -> str:
        """
        Generate a unique output path that doesn't exist.

        Args:
            file_path: target output file 
            extension: File extension including the dot

        Returns:
            A unique file path that doesn't exist
        """
                
        base_path, _ = os.path.splitext(file_path)

        counter = 0
        while True:
            if counter == 0:
                path = f"{base_path}{extension}"
            else:
                path = f"{base_path+'_'+rename}{'' if counter == 1 else f'-{counter-1}'}{extension}"
            if not os.path.exists(path):
                return path
            counter += 1

    def get_metadata(self, file_path: str) -> dict:
        """
        Get metadata of the file.

        Args:
            file_path: Path to the file.

        Returns:
            Metadata of the file.

        Raises:
            ffmpeg.Error: If metadata retrieval fails
        """
        try:
            return self.ffmpeg_cmd.probe(file_path, cmd=FFPROBE_PATH)
        except ffmpeg.Error as e:
            error_message = e.stderr.decode('utf-8')
            self.logger.error(f"Error retrieving metadata for {file_path}: {error_message}")
            raise


class Stats:
    def __init__(self, input_file, output_file, logger: logger = None): # type: ignore
        """
        Initialize the AudioDecoder with input and output file paths.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.logger = logger if logger is not None else get_logger(__name__)

    def get_file_size(self, file_path):
        """
        Get the size of a file in bytes.
        """
        return os.path.getsize(file_path)

    def format_size(self, size_bytes):
        """
        Convert file size to a human-readable format (e.g., KB, MB).
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

    def compare_file_sizes(self):
        """
        Compare the sizes of the input and output files.
        """
        input_size = self.get_file_size(self.input_file)
        output_size = self.get_file_size(self.output_file)

        logger.debug(f"Source file size: {self.format_size(input_size)}")
        logger.debug(f"Output file size: {self.format_size(output_size)}")

        size_difference = output_size - input_size
        size_ratio = output_size / input_size

        if size_difference > 0:
            logger.info(f"The output file is {self.format_size(size_difference)} larger than the source file.")
        elif size_difference < 0:
            logger.info(f"The output file is {self.format_size(abs(size_difference))} smaller than the source file.")
        else:
            logger.info("The output file is the same size as the source file.")

        logger.success(f"Size ratio (output/source): {size_ratio:.2f}")


class FFmpegCommand:
    
    def __init__(self, ffmpeg_path="ffmpeg", logger: logger = None): # type: ignore
        """Initialize the FFmpeg command builder."""
        self.ffmpeg_path = ffmpeg_path
        self.input_file = None
        self.output_file = None  # optional
        self.metadata_options = {}
        self.output_options = {}
        self.global_options = ["-y", "-hide_banner", "-loglevel", "info"]  # Default global options
        self.logger = logger if logger is not None else get_logger(__name__)

    def input(self, input_file):
        """Set the input file."""
        self.input_file = input_file
        return self  # Fluent API

    def output(self, output_file):
        """Set the output file (optional)."""
        self.output_file = output_file
        return self  # Fluent API

    def metadata(self, metadata_dict):
        """Set metadata options."""
        if metadata_dict:
            self.metadata_options.update(metadata_dict)
        return self  # Fluent API

    def output_args(self, output_dict):
        """Set output encoding options."""
        self.output_options.update(output_dict)
        return self  # Fluent API

    def global_args(self, global_list):
        """Set global FFmpeg options."""
        self.global_options = global_list
        return self  # Fluent API

    def compile(self):
        """Constructs the FFmpeg command."""
        if not self.input_file:
            raise ValueError("Input file must be set.")

        # Default output file if not set
        if not self.output_file:
            self.output_file = self.input_file

        # important the order
        command = [self.ffmpeg_path] + ["-i", self.input_file] + self.global_options 

        # Add metadata
        for key, value in self.metadata_options.items():
            command.extend(["-metadata", f"{key}={value}"])

        # Add output options
        for key, value in self.output_options.items():
            command.extend([f"-{key}", value])

        # Set output file
        command.append(self.output_file)

        return command

    def run(self, capture_stdout=False, capture_stderr=False):
        """Run the FFmpeg command."""
        command = self.compile()
        
        # Set subprocess options for capturing output
        stdout_option = subprocess.PIPE if capture_stdout else None
        stderr_option = subprocess.PIPE if capture_stderr else None
                
        try:
            self.logger.debug("Running FFmpeg command:", " ".join(command))
            process = subprocess.run(command, check=True, stdout=stdout_option, stderr=stderr_option, text=True)
            self.logger.success(f"Executed: {self.output_file}")
            return process.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed with error: {e.stderr}")
            raise

    def probe(self, output_file, cmd:str=None):
        """Probe the output file to check media info."""
        if not output_file:
            raise ValueError("Output file must be set before probing.")
        try:
            info = ffmpeg.probe(output_file, cmd=cmd)
            return info
        except ffmpeg.Error as e:
            self.logger.error("Error probing file:", e)
            raise