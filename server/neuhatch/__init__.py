from flask import Flask
from neuhatch.config import get_default_config

config = get_default_config()
app = Flask(__name__)
app.secret_key = config.app_secret
import neuhatch.views
