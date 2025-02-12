from utils import JsonLoader
from typing import Dict, List
from models import Profile, Argument   

class ProfileDataManager:

    def __init__(self):        
        self.profiles: List[Profile] = None
        self.arguments: List[Argument] = None

    def load_profiles(self, profiles_path: str) :
        data = JsonLoader(profiles_path).load()
        profiles_lst = []
        for profile in data["Profiles"]:
            profile_obj = Profile(
                Name=profile["Name"],
                Codec=profile["Codec"],
                Extension=profile["Extension"],
                FFmpegSetup=profile["FFmpegSetup"],
                SizeFactor=float(profile["SizeFactor"]),
                CpuFactor=float(profile["CpuFactor"]),
                Description=profile["Description"]
            )
            profiles_lst.append(profile_obj)            
        self.profiles = profiles_lst
        return self

    def load_arguments(self, globals_args_path: str):
        data =  JsonLoader(globals_args_path).load()
        self.arguments = [Argument(**argument) for argument in data]
        return self

    def get_profile_by_name(self, profile_name: str) -> Profile:
        for profile in self.profiles:
            if profile_name.lower() == profile.Name.lower():
                return profile
        raise ValueError(f"Profile '{profile_name}' not found")

    def get_profiles_by_codec(self, codec: str) -> List[Profile]:
        profiles = []
        for profile in self.profiles:
            if profile.Codec.lower() == codec.lower():
                profiles.append(profile)
        return profiles

    def get_profiles_by_extension(self, extension: str) -> List[Profile]:
        profiles = []
        for profile in self.profiles:
            if profile.Extension.lower() == extension.lower():
                profiles.append(profile)
        return profiles
    
    @staticmethod
    def get_FFmpegSetup_as_dict(profile:Profile)->Dict[str,str]:
        # Return FFmpegSetup as dict str
        return dict(item.strip().split("=") for item in profile.FFmpegSetup.split(","))

    def get_arguments_as_dict(self)->Dict[str,str]:
        arguments_as_dic: Dict[str, Argument] = {}
        for argument in self.arguments:
            arguments_as_dic[argument.Name] = argument.Default
        return arguments_as_dic
        

    

    
