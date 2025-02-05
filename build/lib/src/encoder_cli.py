#!/usr/bin/env python3
import argparse
import os
import sys

# Add the src directory to the Python path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_dir)

from src.data_manager import ProfilesDataManager  # noqa: E402

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)



def main():
    parser = argparse.ArgumentParser(description='Media Encoder CLI')
    parser.add_argument('--profile', '-p', help='Audio profile name', default='default')
    parser.add_argument('--list-profiles', '-l', action='store_true', help='List available audio profiles')
    parser.add_argument('input', nargs='?', help='Input file path')
    parser.add_argument('output', nargs='?', help='Output file path')
    
    args = parser.parse_args()
    
    profiles_path = get_resource_path("config/ffmpeg.audio.profiles.json")
    data_manager = ProfilesDataManager(profiles_path)
    
    if args.list_profiles:
        profiles = data_manager.get_all_profiles()
        print("\nAvailable Audio Profiles:")
        for profile in profiles:
            print(f"- {profile.Profile}")
            print(f"  Codec: {profile.Codec}")
            print(f"  Extension: {profile.Extension}")
            print(f"  FFmpeg Setup: {profile.FFmpegSetup}")
            print(f"  Size Factor: {profile.SizeFactor}")
            print(f"  CPU Factor: {profile.CpuFactor}")
            print(f"  Description: {profile.Description}")
            print()
        return
    
    if not args.input or not args.output:
        parser.error("Both input and output files are required when not using --list-profiles")
    
    try:
        profile = data_manager.get_profile_by_name(args.profile)
        if not profile:
            print(f"Error: Profile '{args.profile}' not found")
            return
        
        print(f"Using profile: {profile.Profile}")
        print(f"Processing {args.input} -> {args.output}")
        
        # Here you would add the actual encoding logic using the profile
        # For example:
        # encoder = AudioEncoder(profile)
        # encoder.encode(args.input, args.output)
        
        print("Encoding complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()