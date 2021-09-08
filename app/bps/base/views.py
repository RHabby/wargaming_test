import os

from app.services.file_analyzer.analyzer import calc_file_stats
from app.services.utils.misc import validate_and_save_file
from flask import Blueprint, flash, redirect, url_for
from flask.templating import render_template

from .forms import FileForm

bp = Blueprint("base", __name__)


@bp.route("/")
def index():
    title = "Index Page"
    form = FileForm()

    return render_template("/base/index.html",
                           form=form,
                           title=title)


@bp.route("/", methods=["POST"])
def upload_file():
    file = None
    title = "TF-IDF"

    form = FileForm()
    if form.validate_on_submit():
        file = validate_and_save_file(file=form.file.data)

    if file:
        stats = calc_file_stats(file=file)[:50]
        return render_template("/base/index.html",
                               form=form,
                               title=title,
                               stats=stats)
    else:
        flash(".txt files only!")
        return redirect(url_for("base.index"))
