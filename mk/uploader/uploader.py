import os
import pathlib

import time

from flask import *
from ..db import *

from ..decorators import user_only

from werkzeug.utils import secure_filename

uploader_bp = Blueprint("uploader", __name__, url_prefix="/uploader")

ALLOWED_FILE_EXTS = [".png", ".jpg", ".gif"]

def file_is_allowed(filename: str):
    print(filename)
    ext = pathlib.Path(filename).suffix
    print(ext)
    return ext in ALLOWED_FILE_EXTS

@uploader_bp.route("/storage/<path:filename>")
@user_only
def storage(filename):
    p = "storage"
    fullp = os.path.join(p, filename)

    if not os.path.exists(p):
        os.makedirs(p)
        return render_template("not_found.html")

    if os.path.exists(fullp):
        return send_from_directory(p, filename)
    else:
        return render_template("not_found.html")

@uploader_bp.route("/upload", methods=["GET", "POST"])
@user_only
def upload_file():
    if request.method == "POST":
        if not "file" in request.files:
            return render_template("not_found.html")

        file = request.files["file"]

        if file.filename == "":
            return render_template("not_found.html")

        filename = secure_filename(file.filename)

        if file_is_allowed(filename):
            actual_filename = str(int(time.time())) + "_" + filename
            p = os.path.join("storage", actual_filename)

            slash_path = "/uploader/storage/" + actual_filename

            file.save(p)
            return render_template("uploads/file_demonstration.html", img_src=slash_path)
        else:
            print(1)
            return render_template("not_found.html")

        return render_template("not_found.html")
    else:
        return render_template("uploads/uploader.html")
