import argparse
import os
import sys
from typing import Tuple
from models import ProfileConstants
from config import FFMPEG_PATH, FFMPEG_PROFILES_PATH
from encoder import Encoder
from data_manager import ProfileDataManager
from utils import create_audio_profiles_table

def check_ffmpeg() -> Tuple[bool, str]:
    """Check if ffmpeg is installed in the dist folder.
    Returns:
        Tuple[bool, str]: (is_installed, message)
    """
    # Get the project root directory (two levels up from this file)
    ffmpeg_path = FFMPEG_PATH    
    if os.path.exists(ffmpeg_path) and os.path.isfile(ffmpeg_path):
        return True, "FFmpeg found in dist folder"
    return False, "FFmpeg not found. Please run build.bat to install FFmpeg"

def show_profiles():
    profiles_path = FFMPEG_PROFILES_PATH 
    data_manager = ProfileDataManager().load_profiles(profiles_path)
    print(create_audio_profiles_table(data_manager.profiles))

def encode(input_file, output_file, profile, metadata):
    try:                
        print(f"Encoding.. {input_file} -> {output_file} -p {profile}")                
        Encoder(profile).encode(input_file, output_file, metadata_tags=kvp_as_dic(metadata))        
        print("Encoding complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
 
def copy(input_file, output_file, metadata_str):
    try:                
        print(f"Copying metadata.. {input_file} -> {output_file} -m {metadata_str}")                
        Encoder(ProfileConstants.AMAZON_MUSIC_HD).copy(input_file, output_file, metadata_tags=kvp_as_dic(metadata_str))        
        print("Copying complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def kvp_as_dic(metadata_str):
    """Dummy function to simulate copying with metadata."""
    metadata = {}
    if metadata_str:  # Check if metadata_str is not empty
        for item in metadata_str.split(','):
            try:
                key, value = item.split('=')
                metadata[key.strip('\'"')] = value.strip('\'"')
            except ValueError:
                raise ValueError(f"Invalid metadata item: {item}")
            
    return metadata

def main():
    
    parser = argparse.ArgumentParser(description="Commnad line..")

    # Positional arguments (input and optional output)
    parser.add_argument("input", nargs="?", help="Input file path.")
    parser.add_argument("output", nargs="?", help="Optional output file path, if not set overwrites the input file)}.")

    # Optional arguments
    parser.add_argument("-o", "--operation", choices=["encode", "copy"], type=str, help="Operation [encode, copy], copy only for metadata copying.")
    parser.add_argument("-p", "--profile", nargs="?", const="default", help="Encoding profile, see more with -p.")
    parser.add_argument("-m", "--metadata", help="Metadata in 'key1=value1, key2=value2' format.")

    args = parser.parse_args()

    #Handle the cases with no Input
    if not args.input:
        
        # case -p without-value
        if args.profile == "default" and not (args.operation or args.metadata or args.output):
            show_profiles()
            print("\nChoose profile below.\n")
            sys.exit(0)
            
        if args.operation:
            print("Error: Input file is required.", file=sys.stderr)
            sys.exit(1)

        if args.operation or args.metadata:
            print("Error: Input file is required.", file=sys.stderr)
            sys.exit(1)

        parser.print_help() #if nothing is provided
        sys.exit(1) #indicate that we exit with error

    # Validate that input is present with other options
    if args.input and not args.operation: 
        print("Error: Requires Operation (-o).", file=sys.stderr)
        sys.exit(1)

    #Check that input is present with output:
    if not args.input and args.output:
        print("Error: Input file is required when using specifying an output file", file=sys.stderr)
        sys.exit(1)

    # Perform actions based on arguments
    if args.operation == "encode":
        if not args.profile or args.profile == "default":
            print("Error: Profile is required for the 'encode' operation.", file=sys.stderr)
            sys.exit(1)
        output_file = args.output if args.output else args.input #set default output
        encode(args.input, output_file, args.profile, args.metadata)

    elif args.operation == "copy":
        if not args.metadata:
            print("Error: Metadata is required for the 'copy' operation.", file=sys.stderr)
            sys.exit(1)
        output_file = args.output if args.output else args.input  #set default output
        copy(args.input, output_file, args.metadata)

    elif args.output: #if only input and output
        print("Error: Requires Operation (-o), with profile (-p), (or/and) metadata (-m).", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()