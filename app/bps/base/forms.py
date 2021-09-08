from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField


class FileForm(FlaskForm):
    file = FileField(label="document",
                     validators=[FileRequired(),
                                 FileAllowed(["txt"], ".txt files only!")]
                     )
    submit = SubmitField("Загрузить")
