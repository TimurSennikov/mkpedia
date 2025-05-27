from .articles import articles_bp
from ..decorators import *
from ..db import *

@articles_bp.route("/article")
@user_only
def get_article():
    artname = request.args.get("article")
    db = get_db()

    if artname is None:
        return render_template("error.html", error="Статья не найдена!")

    art = db.execute("SELECT * FROM articles WHERE title = ?", (artname,)).fetchone()
    if not art:
        return render_template("error.html", error="Статья не найдена!")

    arts = json.loads(art["data"])

    if art is None:
        return render_template("error.html", error="Статья не найдена!")

    with open(arts[-1]["body"]) as f:
        return render_template("articles/article.html", title=art["title"], article=f.read(), last_edit_by=arts[-1]["last_edit_by"])
