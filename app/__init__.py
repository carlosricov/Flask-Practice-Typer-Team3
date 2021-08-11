from datetime import timedelta
from functools import wraps
from logging import log
from flask import (
    Flask,
    render_template,
    Response,
    request,
    redirect,
    url_for,
    session,
    flash,
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from app.db import get_db
from decouple import config
import os

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(os.getcwd(), "flask.sqlite")

# Key for keeping client/server connection secure.
secretKey = config("secretKey", default="")
app.secret_key = secretKey

# Keep the user logged in.
app.permanent_session_lifetime = timedelta(hours=24)

db.init_app(app)

# We must confirm the user logs in before accessing the dashboard.
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Login required")
            return redirect(url_for("login"))

    return wrap


# Landing page.
@app.route("/")
def index():
    return render_template("index.html")


# Health Checkpoint.
@app.route("/health", methods=["GET"])
def health():
    return Response("Something Here"), 200


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session["logged_in"] = True
            return redirect(url_for("dash")), 200
        else:
            flash(error)
            return render_template("login.html"), 418

    return render_template("login.html")


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
            is not None
        ):
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return render_template("index.html")
        else:
            return error, 418

    return render_template("register.html")


# More pages go below here.
@app.route("/dash/home")
@login_required
def dash():
    return render_template("/dash/home.html")


@app.route("/dash/typer")
@login_required
def typer():
    return render_template("/dash/typer.html")


@app.route("/dash/settings")
@login_required
def settings():
    return render_template("/dash/settings.html")


@app.route("/dash/settings/edit")
@login_required
def edit():
    return render_template("/dash/settings/edit.html")
