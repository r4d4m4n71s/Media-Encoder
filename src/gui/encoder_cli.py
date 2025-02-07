#!/usr/bin/env python3
import argparse
import os
import sys
from typing import Tuple
from tabulate import tabulate
from config import *
from models import ProfileConstants
from encoder import Encoder

# Add the src directory to the Python path
# src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, src_dir)

from data_manager import ProfileDataManager  # noqa: E402
from models import Profile # noqa: E402

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

def create_audio_profiles_table(profiles:dict[str,Profile]) -> str:
    headers = ["Profile", "Codec", "Extension", "FFmpeg Setup", "Size Factor", "CPU Factor", "Description"]
    rows = []
    for profile in profiles:
        rows.append([
            profile.Name,
            profile.Codec,
            profile.Extension,
            profile.FFmpegSetup,
            profile.SizeFactor,
            profile.CpuFactor,
            profile.Description
        ])
    return tabulate(rows, headers, tablefmt="github")


def main():
    # Check FFmpeg first
    ffmpeg_installed, ffmpeg_message = check_ffmpeg()
    if not ffmpeg_installed:
        print("\nError: FFmpeg Check Failed")
        print(ffmpeg_message)
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Media Encoder CLI')
    parser.add_argument('--profiles', '-p', action='store_true', help='List available audio profiles')
    parser.add_argument('input', nargs='?', help='Input file path')
    parser.add_argument('output', nargs='?', help='Output file path')
    parser.add_argument('profile', nargs='?', help='Audio profile name', default='default')
    

    args = parser.parse_args()
    
    profiles_path = FFMPEG_PROFILES_PATH 
    data_manager = ProfileDataManager().load_profiles(profiles_path)
    
    if args.profiles:
        print("\nAvailable Audio Profiles:")
        print(f"\n{create_audio_profiles_table(data_manager.profiles)}\n")        
        print("\nUsage: encoder inputFile outputFile \"AudioProfile\" \n")   
        return
    
    if not args.input or not args.output:
        parser.error("Both input and output files are required when not using --help")
    
    try:
                
        print(f"Processing {args.input} -> {args.output}")        
        Encoder(args.profile).reencode(args.input, args.output)        
        print("Encoding complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()