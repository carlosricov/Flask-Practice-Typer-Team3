from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=('GET', 'POST'))
def login():
    return render_template("login.html")

@app.route("/register", methods=('GET', 'POST'))
def register():
    return render_template("register.html")

# Health Checkpoint.
@app.route("/health", methods=["GET"])
def health():
    return Response("Something Here"), 200


# More pages go below here.
