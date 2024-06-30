import configparser
import os
import json

class ApiConfigParser(object):
    def __init__(self,path):
        self.config = configparser.ConfigParser()
        self.config.read(str(path))
    def get_config(self,config_name):
        return self.config["api_project"][config_name]
    def get_list_project_config(self):
        return self.config["api_project"]
def extract_my_data(path,ext,with_index=False):
    folder_path = os.path.abspath(path)
    valid_data = []
    for file in os.listdir(folder_path):
        filename = os.fsdecode(file)
        if not filename.endswith(ext):
            continue

        with open(os.path.join(folder_path,filename)) as my_file_json:
            data = json.load(my_file_json)
            valid_data.append(data)

    if (with_index == True):
        return list(enumerate(valid_data,start=1))
    return valid_data
def extract_my_json(path):
    return extract_my_data(path,".json")