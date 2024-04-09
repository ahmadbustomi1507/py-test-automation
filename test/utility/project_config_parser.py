import configparser


class ProjectConfigParser(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("pytest.ini")
    def get_config(self,config_name):
        return self.config["project"][config_name]

    def get_list_project_config(self):
        return self.config["project"]