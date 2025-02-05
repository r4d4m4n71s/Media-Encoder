from loguru import logger

# Configure the shared logger
logger.add("app.log", rotation="5 MB", level="DEBUG", format="{time} {level} {message}", enqueue=True)

# Function to get the logger
def get_logger(name):
    return logger.bind(module=name)

FFMPEG_PROFILES_PATH = "src/config/ffmpeg.audio.profiles.json"
FFMPEG_GLOBALARGS_PATH = "config/_ffmpeg.global.arguments.json"
