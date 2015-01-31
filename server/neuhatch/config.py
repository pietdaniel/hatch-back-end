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
    def environ_set(self):
        self.consumer_key = os.environ.get("consumer_key")
        self.consumer_secret = os.environ.get("consumer_secret")
        self.access_token = os.environ.get("access_token")
        self.access_token_secret = os.environ.get("access_token_secret")
        self.app_secret = os.environ.get('app_secret')

        self.print_warning("consumer_key")
        self.print_warning("consumer_secret")
        self.print_warning("access_token")
        self.print_warning("access_token_secret")
        self.print_warning("app_secret")

    def print_warning(self, var):
        if eval("self.%s" % var) is None:
            print "Warning %s is None" % var


