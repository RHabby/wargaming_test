import os

from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


def validate_and_save_file(file: FileStorage) -> str:
    filename = secure_filename(file.filename)
    path_to_save = os.path.join(current_app.config["UPLOAD_FOLDER"],
                                filename)
    file.save(path_to_save)

    return path_to_save
