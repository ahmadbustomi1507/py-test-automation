class Config(object):
    def __init__(self, env):

        if env is not None:
            self.base_url = {
                'dev':'https//mydev-env.com',
                'qa':'https//myqa-env.com'
            }[env]

            self.app_port ={
                'dev': 8080,
                'qa' : 80
            }[env]
        else:
            self.base_url = 'https//mydev-env.com'
            self.app_port = 8080