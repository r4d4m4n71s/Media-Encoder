from tabulate import tabulate
from models import Profile

def create_audio_profiles_table(data: list[Profile]) -> str:
    headers = ["Profile", "Codec", "Extension", "FFmpeg Setup", "Size Factor", "CPU Factor", "Description"]
    rows = []
    for profile in data:
        rows.append([
            profile.Profile,
            profile.Codec,
            profile.Extension,
            profile.FFmpegSetup,
            profile.SizeFactor,
            profile.CpuFactor,
            profile.Description
        ])
    return tabulate(rows, headers, tablefmt="github")