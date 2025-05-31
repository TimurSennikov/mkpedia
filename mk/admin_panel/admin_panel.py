from flask import *

from ..db import *

from ..decorators import admin_only, root_only

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/panel", methods=["GET", "POST"])
@admin_only
def render_panel():
    if request.method == "POST":
        if not g.user["username"] == "root":
            return render_template("not_admin.html")

        newpwd = request.form["new_password"]

        if not newpwd:
            return render_template("not_found.html")

        db = get_db()

        db.execute("UPDATE users SET password = ? WHERE username = 'root'", (newpwd,))
        db.commit()

        session.clear()

    db = get_db()
    queue = db.execute("SELECT * FROM queue").fetchall()
    return render_template("/admin/panel.html", queue=queue, is_root=g.user["username"]=="root")

@admin_bp.route("/reject", methods=["GET"])
@admin_only
def reject():
    db = get_db()

    username = request.args.get("username")

    if not username:
        return "Пожалуйста, укажите username в query-параметрах, или, блять, используйте админ панель так, как это задумал админ, сука."

    db.execute("DELETE FROM queue WHERE username = ?", (username,))
    db.commit()

    return redirect(url_for("admin.render_panel"))

@admin_bp.route("/accept", methods=["GET"])
@admin_only
def accept():
    db = get_db()

    username = request.args.get("username")

    if not username:
        return "Сучара, эту страницу грузи только кнопками с админ-панели, если не знаешь, что делать, блять."

    q = db.execute("SELECT * FROM queue WHERE username = ?", (username,)).fetchone()
    password = q["password"]

    db.execute("DELETE FROM queue WHERE username = ?", (username,))
    db.execute("INSERT INTO users VALUES (?, ?, 0, ?, 0)", (username, password, ""))

    db.commit()

    return redirect(url_for("admin.render_panel"))
