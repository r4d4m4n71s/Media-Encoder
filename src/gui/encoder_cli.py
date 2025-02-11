import argparse
import os
import sys
from typing import Tuple
from models import ProfileConstants
from config import FFMPEG_PATH, FFMPEG_PROFILES_PATH
from encoder import Encoder
from data_manager import ProfileDataManager
from gui.__init__ import create_audio_profiles_table

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
    print(create_audio_profiles_table(data_manager))

def encode(input_file, output_file, profile, metadata):
    try:                
        print(f"Encoding.. {input_file} -> {output_file} -p {profile}")                
        Encoder(profile).encode(input_file, output_file, metadata_tags=metadata)        
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
                metadata[key.strip()] = value.strip()
            except ValueError:
                raise ValueError(f"Invalid metadata item: {item}")
            
    return metadata

def main():
    
    parser = argparse.ArgumentParser(description="Process files with various operations.")

    # Positional arguments (input and optional output)
    parser.add_argument("input", nargs="?", help="Input file path.")
    parser.add_argument("output", nargs="?", help="Optional output file path.")

    # Optional arguments
    parser.add_argument("-o", "--operation", choices=["encode", "copy"], help="Operation to perform: encode or copy.")
    parser.add_argument("-p", "--profile", help="Profile to use for encoding.")
    parser.add_argument("-m", "--metadata", help="Metadata in 'key=value,key2=value2' format.")

    args = parser.parse_args()

    #Handle the cases with no Input
    if not args.input:
        if args.profile:
            show_profiles()
            sys.exit(0)

        if args.operation:
            print("Error: Input file is required to specify an operation", file=sys.stderr)
            sys.exit(1)

        if args.operation or args.metadata:
            print("Error: Input file is required with other options.", file=sys.stderr)
            sys.exit(1)

        parser.print_help() #if nothing is provided
        sys.exit(1) #indicate that we exit with error

    # Validate that input is present with other options
    if args.input and not (args.operation or args.profile or args.metadata or args.output):
        print("Error: Operation (-o), profile (-p), metadata (-m), or output file is required with input file.", file=sys.stderr)
        sys.exit(1)

    #Check that input is present with output:
    if not args.input and args.output:
        print("Error: Input file is required when using specifying an output file", file=sys.stderr)
        sys.exit(1)

    # Perform actions based on arguments
    if args.operation == "encode":
        if not args.profile:
            print("Error: Profile is required for the 'encode' operation.", file=sys.stderr)
            sys.exit(1)
        output_file = args.output if args.output else "output.encoded" #set default output name
        encode(args.input, output_file, args.profile)

    elif args.operation == "copy":
        if not args.metadata:
            print("Error: Metadata is required for the 'copy' operation.", file=sys.stderr)
            sys.exit(1)
        output_file = args.output if args.output else "output.copied"  #set default output name
        copy(args.input, output_file, args.metadata)

    elif args.profile:
        show_profiles()  # Show profiles if only -p is provided after input.

    elif args.output: #if only input and output
        print("Error: Provide.. Operation (-o), profile (-p), metadata (-m).", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()