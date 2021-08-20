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
from flask_toastr import Toastr

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(os.getcwd(), "flask.sqlite")

# Key for keeping client/server connection secure.
secretKey = config("secretKey", default="")
app.secret_key = secretKey

# Keep the user logged in.
app.permanent_session_lifetime = timedelta(hours=24)

db.init_app(app)

# Toastr initialize.
toastr = Toastr(app)

# We must confirm the user logs in before accessing the dashboard.
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Login required", "warning")
            return redirect(url_for("login"))

    return wrap


# Landing page.
@app.route("/")
def index():
    if "logged_in" in session:
        flash("User is logged in.")
        return redirect(url_for("dash"))

    return render_template("index.html")


# Health Checkpoint.
@app.route("/health", methods=["GET"])
def health():
    return Response("Something Here"), 200


@app.route("/login", methods=("GET", "POST"))
def login():
    if "logged_in" in session:
        flash("User is logged in.")

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password"

        if error is None:
            session["logged_in"] = True
            flash(f"User {username} logged in!", "success")
            return render_template("/dash/home.html")
        else:
            flash("Incorrect username or password", "error")
            return render_template("login.html"), 418

    return render_template("login.html")


@app.route("/register", methods=("GET", "POST"))
def register():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = 0

        if not username:
            error = 1
        elif not password:
            error = 2
        elif (
            db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
            is not None
        ):
            error = 3

        if error == 0:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            flash(f"User {username} created successfully", "success")
            return render_template("index.html")
        elif error == 1:
            flash("Username is required", "error")
            return render_template("register.html"), 418
        elif error == 2:
            flash("Password is required", "error")
            return render_template("register.html"), 418
        elif error == 3:
            flash(f"User {username} is already registered.", "error")
            return render_template("register.html"), 418
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


@app.route("/dash/signout")
@login_required
def sign_out():
    session.pop("logged_in", None)
    flash("User succesfully logged out.")
    return render_template("index.html")
