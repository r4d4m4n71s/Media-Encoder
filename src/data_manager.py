from utils import JsonLoader
from typing import List
from models import Profiles, Profile   

class ProfilesDataManager:
    def __init__(self, profiles_path: str):        
        self.profiles_data = ProfilesDataManager.load_profiles(profiles_path)

    def get_profile_by_name(self, profile_name: str) -> Profile:
        if profile_name in self.profiles_data.profiles:
            return self.profiles_data.profiles[profile_name]
        raise ValueError(f"Profile '{profile_name}' not found")

    def get_profiles_by_codec(self, codec: str) -> List[Profile]:
        return [profile for profile in self.profiles_data.profiles.values() if profile.Codec.lower() == codec.lower()]

    def get_profiles_by_extension(self, extension: str) -> List[Profile]:
        return [profile for profile in self.profiles_data.profiles.values() if profile.Extension.lower() == extension.lower()]

    def get_all_profiles(self) -> List[Profile]:
        # Return a new list to prevent modification of the original data
        return list(self.profiles_data.profiles.values())

    @staticmethod
    def load_profiles(profiles_path: str) -> Profiles:
        data = JsonLoader(profiles_path).load()
        profiles_dict = {}
        for profile in data["profiles"]:
            profile_obj = Profile(
                Profile=profile["Profile"],
                Codec=profile["Codec"],
                Extension=profile["Extension"],
                FFmpegSetup=profile["FFmpegSetup"],
                SizeFactor=float(profile["SizeFactor"]),
                CpuFactor=float(profile["CpuFactor"]),
                Description=profile["Description"]
            )
            profiles_dict[profile["Profile"]] = profile_obj
        return Profiles(profiles=profiles_dict)