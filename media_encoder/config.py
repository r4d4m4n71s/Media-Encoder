import os
import sys
from loguru import logger

def resolve_root(path:str):    
    #check if virtual environment is enabled
    #if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        #return os.path.join(os.environ.get("VIRTUAL_ENV", path))

    return os.path.join(os.getcwd(), path)

FFMPEG_PATH = os.environ.get("FFMPEG_PATH", resolve_root("build/ffmpeg.exe"))
FFPROBE_PATH = os.environ.get("FFPROBE_PATH", resolve_root("build/ffprobe.exe"))
FFMPEG_PROFILES_PATH = os.environ.get("FFMPEG_PROFILES_PATH", resolve_root("media_encoder/_config/ffmpeg.audio.profiles.json"))
FFMPEG_GLOBALARGS_PATH = os.environ.get("FFMPEG_GLOBALARGS_PATH", resolve_root("media_encoder/_config/ffmpeg.audio.arguments.json"))
MUTAGEN_AUDIO_TAGS = os.environ.get("MUTAGEN_AUDIO_TAGS", resolve_root("media_encoder/_config/mutagen.audio.tags.json"))


# Configure the shared logger
logger.add("app.log", rotation="5 MB", level="DEBUG", format="{time} {level} {message}", enqueue=True)

# Function to get the logger
def get_logger(name):
    return logger.bind(module=name)