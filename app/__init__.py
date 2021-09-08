from flask import Flask

from .bps.base.views import bp as base_blueprint

UPLOAD_FOLDER = "app/static/files/"
SECRET = "very-secret-key-for-myApp"


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["SECRET_KEY"] = SECRET

    app.register_blueprint(blueprint=base_blueprint)
    
    return app
