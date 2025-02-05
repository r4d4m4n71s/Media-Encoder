from config.create_readme import create_audio_profiles_table
from data_manager import ProfilesDataManager
import os

def update_readme():
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Load profiles
    profiles_path = os.path.join(current_dir, "config", "ffmpeg.audio.profiles.json")
    profiles_manager = ProfilesDataManager(profiles_path)
    profiles = profiles_manager.get_all_profiles()
    
    # Generate profiles table
    profiles_table = create_audio_profiles_table(profiles)
    
    # Read existing README
    readme_path = os.path.join(project_root, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace profiles table placeholder
    updated_content = content.replace("{profiles_table}", profiles_table)
    
    # Write updated README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_readme()