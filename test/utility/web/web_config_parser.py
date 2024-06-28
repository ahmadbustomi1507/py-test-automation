import configparser

class WebConfigParser(object):
    def __init__(self,path):
        self.config = configparser.ConfigParser()
        self.config.read(str(path))
    def get_config(self,config_name):
        return self.config["web_project"][config_name]
    def get_list_project_config(self):
        return self.config["web_project"]
