from tabulate import tabulate
from media_encoder.models import Profile

def create_audio_profiles_table(profiles:list[Profile]) -> str:
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