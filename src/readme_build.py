from tabulate import tabulate
from data_manager import ProfilesDataManager
from models import Profile
from __init__ import FFMPEG_PROFILES_PATH


def get_project_info():
    
    project_name = "Media encoder: "
    description = "Profiles:"

    data = ProfilesDataManager(FFMPEG_PROFILES_PATH).get_all_profiles()        
    profiles_table = create_audio_profile_table(data)
    installation = "Enter the installation instructions: "
    usage = "GNU GENERAL PUBLIC LICENSE"
    license = "Enter the license information: "
    
    return {
        "project_name": project_name,
        "description": description,
        "profiles_table": profiles_table,
        "installation": installation,
        "usage": usage,
        "license": license
    }

def create_readme(info):
    readme_content = f"""
# {info['project_name']}

## Description
{info['description']}

{info['profiles_table']}

## Installation
{info['installation']}

## Usage
{info['usage']}

## License
{info['license']}
    """

    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

def create_audio_profile_table(data: list[Profile]):
    headers = ["Profile", "Codec", "Extension", "FFmpeg Setup", "Size Factor", "CPU Factor", "Description"]
    rows = []
    for profile in data:
        rows.append([profile.Profile, profile.Codec, profile.Extension, profile.FFmpegSetup, profile.SizeFactor, profile.CpuFactor, profile.Description])

    table = tabulate(rows, headers, tablefmt="github")
    return table 

if __name__ == "__main__":
    project_info = get_project_info()
    create_readme(project_info)
    print("README.md file has been created successfully!")



