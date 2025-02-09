import os
from loguru import logger

def resolve_to_root(path:str):
    return os.path.join(os.getcwd(), path)

FFMPEG_PATH = os.environ.get("FFMPEG_PATH", resolve_to_root("dist/ffmpeg.exe"))
FFPROBE_PATH = os.environ.get("FFPROBE_PATH", resolve_to_root("dist/ffprobe.exe"))
FFMPEG_PROFILES_PATH = os.environ.get("FFMPEG_PROFILES_PATH", resolve_to_root("src/config/ffmpeg.audio.profiles.json"))
FFMPEG_GLOBALARGS_PATH = os.environ.get("FFMPEG_GLOBALARGS_PATH", resolve_to_root("src/config/ffmpeg.audio.arguments.json"))
MUTAGEN_AUDIO_TAGS = os.environ.get("MUTAGEN_AUDIO_TAGS", resolve_to_root("src/config/mutagen.audio.tags.json"))


# Configure the shared logger
logger.add("app.log", rotation="5 MB", level="DEBUG", format="{time} {level} {message}", enqueue=True)

# Function to get the logger
def get_logger(name):
    return logger.bind(module=name)