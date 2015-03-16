from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.login import LoginManager

def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    http://flask.pocoo.org/snippets/83/
    """
    app = Flask(import_name, instance_relative_config=True, **kwargs)
    app.config.from_pyfile('application.cfg', silent=False)

    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
        return response

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

app = make_json_app(__name__)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import neuhatch.views
import neuhatch.models
