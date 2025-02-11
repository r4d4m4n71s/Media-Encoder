import os

from data_manager import ProfileDataManager  # noqa: E402
from encoder_cli import create_audio_profiles_table  # noqa: E402
from config import FFMPEG_PROFILES_PATH

def update_readme():
    # Get the project root directory
    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(src_dir)    
    # Load profiles
    template_path = os.path.join(src_dir, "config", "readme.template.md")
    readme_path = os.path.join(project_root, "README.md")    
    profiles_path = FFMPEG_PROFILES_PATH
    profiles = ProfileDataManager().load_profiles(profiles_path)
    
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



if __name__ == "__main__":
    update_readme()