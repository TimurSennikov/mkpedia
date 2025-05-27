import json

from .articles import articles_bp
from ..decorators import *
from ..db import *

@articles_bp.route("/getbody")
@user_only
def get_body():
    title = request.args.get("name")

    if not title:
        return render_template("error.html", error="Не указан параметр name.")

    db = get_db()

    art = db.execute("SELECT * FROM articles WHERE title = ?", (title,)).fetchone()

    if not art:
        return render_template("not_found.html"), 404

    with open(json.loads(art["data"])[-1]["body"]) as f:
        return f.read()

@articles_bp.route("/waybackbody")
@admin_only
def wayback_body():
    title = request.args.get("name")
    n = request.args.get("n")

    if not title:
        return render_template("error.html", error="Не указан параметр name.")

    db = get_db()

    art = db.execute("SELECT * FROM articles WHERE title = ?", (title,)).fetchone()

    if not art:
        return render_template("not_found.html"), 404

    arts = json.loads(art["data"])

    try:
        n = int(n)

        if n < 0 or n > len(arts)-1:
            return render_template("not_found.html"), 404

        with open(arts[n]["body"]) as f:
            return f.read()
    except:
        return render_template("not_found.html"), 404
