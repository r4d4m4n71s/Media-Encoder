import os
from data_manager import ProfileDataManager
from tabulate import tabulate
from models import Profile

def update_readme():
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Load profiles
    template_path = os.path.join(current_dir, "config", "readme.template.md")
    readme_path = os.path.join(project_root, "README.md")    
    profiles_path = os.path.join(current_dir, "config", "ffmpeg.audio.profiles.json")
    profiles_manager = ProfileDataManager(profiles_path)
    profiles = profiles_manager.get_all_profiles()
    
    # Generate profiles table
    profiles_table = create_audio_profiles_table(profiles)
    
    # Read existing README
    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace profiles table placeholder
    updated_content = content.replace("{profiles_table}", profiles_table)
    
    # Write updated README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("README.md successfully updated!")    

def create_audio_profiles_table(data: list[Profile]) -> str:
    headers = ["Profile", "Codec", "Extension", "FFmpeg Setup", "Size Factor", "CPU Factor", "Description"]
    rows = []
    for profile in data:
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


if __name__ == "__main__":
    update_readme()