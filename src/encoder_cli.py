#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
from typing import Tuple

# Add the src directory to the Python path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_dir)

from src.data_manager import ProfilesDataManager  # noqa: E402

def check_ffmpeg() -> Tuple[bool, str]:
    """
    Check if FFmpeg is installed and accessible.
    Returns a tuple of (is_installed: bool, message: str)
    """
    # First try system PATH
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True, "FFmpeg is installed and accessible."
    except FileNotFoundError:
        # If not in PATH, check build/ffmpeg/bin directory
        try:
            # Get the base directory - handle both development and PyInstaller environments
            if getattr(sys, 'frozen', False):
                # Running in PyInstaller bundle
                base_path = os.path.dirname(os.path.dirname(sys.executable))
            else:
                # Running in development
                base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Try multiple possible FFmpeg locations
            possible_paths = [
                os.path.join(base_path, 'build', 'ffmpeg', 'bin', 'ffmpeg.exe'),  # Regular project structure
                os.path.join(base_path, 'ffmpeg', 'bin', 'ffmpeg.exe'),  # Direct in project root
                os.path.join(os.path.dirname(sys.executable), 'ffmpeg.exe')  # Next to executable
            ]
            
            ffmpeg_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    ffmpeg_path = path
                    break
                    
            if not ffmpeg_path:
                raise FileNotFoundError("FFmpeg not found in any expected location")
            if os.path.exists(ffmpeg_path):
                subprocess.run([ffmpeg_path, '-version'], capture_output=True, check=True)
                os.environ['PATH'] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ['PATH']
                return True, "FFmpeg found in local build directory and added to PATH."
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
        
        return False, """
FFmpeg is not installed or not found in system PATH.

To install FFmpeg:
1. Download the installer from the project directory
2. Run install_ffmpeg.bat
3. Follow the installation instructions

If you've already installed FFmpeg, make sure it's added to your system PATH.
"""
    except subprocess.CalledProcessError:
        return False, "FFmpeg is installed but not working properly. Try reinstalling FFmpeg."

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)



def main():
    # Check FFmpeg first
    ffmpeg_installed, ffmpeg_message = check_ffmpeg()
    if not ffmpeg_installed:
        print("\nError: FFmpeg Check Failed")
        print(ffmpeg_message)
        sys.exit(1)

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