import ffmpeg
import os
from typing import List, Dict, Optional
from loguru import logger
from data_manager import ProfileDataManager
from config import *

class EncodingError(Exception):
    """Custom exception for processing errors."""
    pass

class Encoder:
    """
    A class to handle encoding and metadata manipulation using FFmpeg.
    """
    def __init__(self, profile_name:str, logger: logger = None): # type: ignore
        """
        Initialize the Reencoder with the codec configuration.

        Args:
            codec: Codec configuration for re-encoding.
            logger: Optional logger instance. If not provided, creates a new one.           

        Raises:
            ValueError: If codec is None or invalid.
        """
        self.logger = logger if logger is not None else get_logger(__name__)

        self.profile = ProfileDataManager().load_profiles(FFMPEG_PROFILES_PATH).get_profile_by_name(profile_name)   
    
    # Use ffmpeg-python to copy streams without re-encoding
    def copy(
        self,
        input_file_path: str,
        output_path: Optional[str] = None,
        delete_original: bool = False,
        metadata_tags: Optional[List[str]] = None,
        ffmpeg_output_args: Optional[Dict[str, str]] = None,
        ffmpeg_global_args: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        self.logger.info("Copying..")
        ffmpeg_output_args.update({'c':'copy'})        
        return self.reencode(input_file_path, output_path, delete_original, metadata_tags, ffmpeg_output_args, ffmpeg_global_args)

    def reencode(
        self,
        input_file_path: str,
        output_path: Optional[str] = None,
        delete_original: bool = False,
        metadata_tags: Optional[List[str]] = None,
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
            output_args: dict[str,str]= ProfileDataManager.get_FFmpegSetup_as_dict(self.profile)
                                                                
            # add user output args
            output_args.update(ffmpeg_output_args or {})
            
            # add user metadata tags
            output_args.update(self._map_metadata(metadata_tags) or {})
                        
            # add default global args
            global_args:dict[str,str] = ProfileDataManager().load_arguments(FFMPEG_GLOBALARGS_PATH).get_arguments_as_dict()      

            # add user global args
            global_args.update(ffmpeg_global_args or {})                        
            
            # format global args
            global_args_formated = self._format_global_args(global_args)
            
            # Create the FFmpeg command
            ffmpeg_command = (
                ffmpeg
                .input(input_file_path)
                .output(output_file_path, **output_args)            
                .global_args(*global_args_formated)
            )            
                        
            # Debug log the final command
            self.logger.debug(f"FFmpeg command: {' '.join(ffmpeg_command.get_args())}")
            
            # Add overwrite flag
            if input_file_path == output_path:
                ffmpeg_command = ffmpeg_command.overwrite_output()
                        
            self.logger.debug(f"Executing FFmpeg command for: {input_file_path}")
            ffmpeg_command.run(capture_stdout=True, capture_stderr=True, cmd=FFMPEG_PATH    )
            self.logger.success(f"Successfully re-encoded: {output_file_path}")

            # check the stats
            Stats(input_file_path, output_file_path).compare_file_sizes()

            # Optionally delete the original file
            if delete_original and input_file_path != output_path:
                try:
                    os.remove(input_file_path)
                    self.logger.debug(f"Deleted original file: {input_file_path}")
                except OSError as e:
                    self.logger.warning(f"Failed to delete original file {input_file_path}: {str(e)}")

        except ffmpeg.Error as e:
            # Handle FFmpeg-specific errors
            error_detail = str(e)
            if hasattr(e, 'stderr') and e.stderr:
                error_detail = e.stderr.decode('utf-8')
            if hasattr(e, 'stdout') and e.stdout:
                stdout = e.stdout.decode('utf-8')
                if stdout:
                    error_detail = f"{error_detail}\n{stdout}" if error_detail else stdout

            self.logger.error(f"FFmpeg error during re-encoding: {input_file_path}:\n{error_detail}")
            raise EncodingError(f"FFmpeg error re-encoding {input_file_path}: {error_detail}") from e
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

    def _map_metadata(self, tags: Optional[List[str]]) -> dict[str,str]:       
        
        metadata_dict:dict[str,str]={}
        if not tags:
            return metadata_dict
        
            if not all(isinstance(tag, str) for tag in tags):
                raise ValueError("All metadata tags must be strings")
            if any(not tag.strip() for tag in tags):
                raise ValueError("Metadata tags cannot be empty strings")
            
        for tag in tags:
            if '=' in tag:
                key, value = tag.split('=', 1)
                metadata_dict.update({key: value})

         # set metadata as argument
        return {f'-metadata:{k}': v for k, v in metadata_dict.items()}                                    

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
            return ffmpeg.probe(file_path)
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

        logger.info(f"Source file size: {self.format_size(input_size)}")
        logger.info(f"Output file size: {self.format_size(output_size)}")

        size_difference = output_size - input_size
        size_ratio = output_size / input_size

        if size_difference > 0:
            logger.info(f"The output file is {self.format_size(size_difference)} larger than the source file.")
        elif size_difference < 0:
            logger.info(f"The output file is {self.format_size(abs(size_difference))} smaller than the source file.")
        else:
            logger.info("The output file is the same size as the source file.")

        logger.success(f"Size ratio (output/source): {size_ratio:.2f}")