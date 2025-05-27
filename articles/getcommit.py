import json

from .articles import articles_bp
from ..decorators import *
from ..db import *

@articles_bp.route("/getcommit")
def get_commit():
    article = request.args.get("article")
    n = request.args.get("n")

    if not article or not n:
        return render_template("error.html", error="Не указан один из или оба параметра (article && n).")

    db = get_db()

    art = db.execute("SELECT * FROM articles WHERE title = ?", (article,)).fetchone()
    if not art:
        return render_template("not_found.html"), 404

    arts = json.loads(art["data"])

    try:
        n = int(n)

        if n < 0 or n > len(arts)-1:
            return render_template("not_found.html"), 404

        our_art = arts[n]

        with open(our_art["body"]) as f:
            return render_template("articles/article.html", title=art["title"], article=f.read(), last_edit_by=our_art["last_edit_by"], wayback_id=n)
    except ValueError as e:
        return render_template("error.html", error="Параметр n должен быть целым числом!")
