from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.login import LoginManager

from neuhatch.config import get_default_config


def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    http://flask.pocoo.org/snippets/83/
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        return response
    app = Flask(import_name, **kwargs)
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error
    return app

config = get_default_config()
app = make_json_app(__name__)
app.secret_key = config.app_secret
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_url
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import neuhatch.views
import neuhatch.models
