from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from functools import wraps
from contextlib import contextmanager

app = Flask(name)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "aeria-development-key"
)

DATABASE = "aeria_users.db"


# DATABASE CONNECTION

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# CREATE DATABASE TABLES

def init_db():
    with get_db() as db:

        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                result TEXT NOT NULL,
                confidence REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)


init_db()


# LOGIN PROTECTION

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return jsonify({
                "error": "Please login first"
            }), 401

        return func(*args, **kwargs)

    return wrapper


# HOME PAGE

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# REGISTER

@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json() or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if len(username) < 3 or len(username) > 20:
        return jsonify({
            "error": "Username must be 3-20 characters"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    hashed_password = generate_password_hash(password)

    try:

        with get_db() as db:

            db.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (username, hashed_password)
            )

        return jsonify({
            "message": "Registration successful!"
        })

    except sqlite3.IntegrityError:

        return jsonify({
            "error": "Username already exists"
        }), 409


# LOGIN

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

    if user and check_password_hash(
        user["password"], password
    ):

        session.clear()

        session["user_id"] = user["id"]
        session["username"] = user["username"]

        return jsonify({
            "message": "Login successful",
            "username": user["username"]
        })

    return jsonify({
        "error": "Invalid username or password"
    }), 401


# CHECK LOGIN

@app.route("/api/me")
def me():

    if "user_id" in session:

        return jsonify({
            "logged_in": True,
            "username": session["username"]
        })

    return jsonify({
        "logged_in": False
    })


# LOGOUT

@app.route("/api/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out"
    })


# AI ANALYSIS

@app.route("/api/analysis", methods=["GET", "POST"])
@login_required
def analysis():

    user_id = session["user_id"]

    # GET LATEST ANALYSIS
    with get_db() as db:

            record = db.execute(
                """
                SELECT result, confidence
                FROM analyses
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (user_id,)
            ).fetchone()

        if record is None:

            return jsonify({
                "class": "Belum dianalisis",
                "confidence": 0
            })

        return jsonify({
            "class": record["result"],
            "confidence": record["confidence"]
        })

    # RECEIVE AI RESULT

    data = request.get_json() or {}

    result = str(data.get("class", "")).strip()

    if not result or len(result) > 100:

        return jsonify({
            "error": "Invalid analysis result"
        }), 400

    try:

        confidence = float(data.get("confidence", 0))

    except (ValueError, TypeError):

        return jsonify({
            "error": "Invalid confidence"
        }), 400

    if not 0 <= confidence <= 100:

        return jsonify({
            "error": "Confidence must be 0-100"
        }), 400

    # SAVE RESULT

    with get_db() as db:

        db.execute(
            """
            INSERT INTO analyses
            (user_id, result, confidence)
            VALUES (?, ?, ?)
            """,
            (user_id, result, confidence)
        )

    return jsonify({
        "received": True,
        "result": {
            "class": result,
            "confidence": confidence
        }
    })


# ANALYSIS HISTORY

@app.route("/api/history", methods=["GET"])
@login_required
def history():

    user_id = session["user_id"]

    with get_db() as db:

        records = db.execute(
            """
            SELECT result, confidence, created_at
            FROM analyses
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 50
            """,
            (user_id,)
        ).fetchall()

    return jsonify({
        "history": [
            {
                "result": row["result"],
                "confidence": row["confidence"],
                "date": row["created_at"]
            }
            for row in records
        ]
    })


# API STATUS

@app.route("/api/status")
def status():

    return jsonify({
        "app": "AERIA AI",
        "status": "online"
    })


# RUN APPLICATION

if name == "main":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )

    if request.method == "GET":
