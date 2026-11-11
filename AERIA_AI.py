from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "aeria-development-key")

DATABASE = "aeria_users.db"

latest_analysis = {
    "class": "Belum dianalisis",
    "confidence": 0
}


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)


init_db()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Please login first"}), 401
        return func(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if len(username) < 3 or len(username) > 20:
        return jsonify({"error": "Username must be 3-20 characters"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    hashed_password = generate_password_hash(password)

    try:
        with get_db() as db:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
        return jsonify({"message": "Registration successful!"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    with get_db() as db:
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    if user and check_password_hash(user["password"], password):
        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return jsonify({
            "message": "Login successful",
            "username": user["username"]
        })

    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/api/me")
def me():
    if "user_id" in session:
        return jsonify({
            "logged_in": True,
            "username": session["username"]
        })

    return jsonify({"logged_in": False})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@app.route("/api/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    global latest_analysis

    if request.method == "GET":
        return jsonify(latest_analysis)

    data = request.get_json() or {}

    latest_analysis = {
        "class": data.get("class", "Unknown"),
        "confidence": data.get("confidence", 0)
    }

    return jsonify({
        "received": True,
        "result": latest_analysis
    })


@app.route("/api/status")
def status():
    return jsonify({
        "app": "AERIA AI",
        "status": "online"
    })


if name == "main":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
