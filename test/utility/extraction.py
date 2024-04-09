import os
import json

CURR_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(CURR_PATH,os.pardir,"resource","data"))
def extract_my_data(path,ext):
    folder_path = os.path.abspath(path)
    valid_data = []
    for file in os.listdir(folder_path):
        filename = os.fsdecode(file)
        if not filename.endswith(ext):
            continue

        with open(os.path.join(folder_path,filename)) as my_file_json:
            data = json.load(my_file_json)
            valid_data.append(data)
    return valid_data

def extract_my_json(path):
    return extract_my_data(path,".json")

