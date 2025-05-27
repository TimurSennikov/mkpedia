import os

from flask import *

from .db import *

from .auth import *
from .admin_panel import *
from .articles import *
from .users import *
from .uploader import *

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="smegma", DATABASE=os.path.join(app.instance_path, "mkpedik.db"), ARTICLE_DIR="article_data")
    app.config.from_pyfile("config.py", silent=True)

    app.config["MAX_CONTENT_LENGTH"] = 50 * 1000 * 1000 # максимальный вес файла - 50 мегабайт.

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(uploader_bp)

    @app.route("/")
    def home():
        return render_template("home.html", article_count=len(get_db().execute("SELECT * FROM articles").fetchall()))

    return app
