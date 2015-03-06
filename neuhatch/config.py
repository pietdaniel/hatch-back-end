import os

def get_default_config():
    c = Config()
    c.environ_set()
    return c

class Config:
    def __init__(self):
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_token_secret = None
        self.app_secret = None
        self.database_url = None
        self.hostname = "http://localhost:5000"

    def environ_set(self):
        self.set_with_warning("consumer_key")
        self.set_with_warning("consumer_secret")
        self.set_with_warning("access_token")
        self.set_with_warning("access_token_secret")
        self.set_with_warning('app_secret')
        self.set_with_warning("database_url")

    def set_with_warning(self, var):
        val = os.environ.get(var)
        setattr(self, var, val)
        if getattr(self, var) is None:
            print "Warning %s is None" % var
