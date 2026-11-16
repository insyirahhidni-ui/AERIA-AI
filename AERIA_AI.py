from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from functools import wraps
from contextlib import contextmanager

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "aeria-development-key"
)

DATABASE = "aeria_users.db"


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
    data = request.get_json(silent=True) or {}

    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

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
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

        return jsonify({
            "message": "Registration successful!"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Username already exists"
        }), 409


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = str(data.get("username", "")).strip()
    password = str(data.get("password", ""))

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

    return jsonify({
        "error": "Invalid username or password"
    }), 401


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

    return jsonify({
        "message": "Logged out"
    })


@app.route("/api/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    user_id = session["user_id"]

    if request.method == "GET":
        with get_db() as db:
            record = db.execute("""
                SELECT result, confidence
                FROM analyses
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 1
            """, (user_id,)).fetchone()
            
        if record is None:
            return jsonify({
                "class": "Belum dianalisis",
                "confidence": 0
            })

        return jsonify({
            "class": record["result"],
            "confidence": record["confidence"]
        })

    data = request.get_json(silent=True) or {}

    result = str(data.get("class", "")).strip()

    if result not in ["penat", "tak penat"]:
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

    with get_db() as db:
        db.execute("""
            INSERT INTO analyses (user_id, result, confidence)
            VALUES (?, ?, ?)
        """, (user_id, result, confidence))

    return jsonify({
        "received": True,
        "result": {
            "class": result,
            "confidence": confidence
        }
    })


@app.route("/api/device-analysis", methods=["POST"])
def device_analysis():
    data = request.get_json(silent=True) or {}

    api_key = os.environ.get("AERIA_DEVICE_KEY")
    username = os.environ.get("AERIA_DEVICE_USERNAME")

    if not api_key or not username:
        return jsonify({"error": "Device not configured"}), 500

    if not data.get("api_key"):
        return jsonify({"error": "API key missing"}), 401

    if data.get("api_key") != api_key:
        return jsonify({"error": "API key mismatch"}), 401

    result = str(data.get("class", "")).strip().lower()

    if result == "tidak penat":
        result = "tak penat"

    if result not in ["penat", "tak penat"]:
        return jsonify({"error": "Invalid class"}), 400

    try:
        confidence = float(data.get("confidence", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid confidence"}), 400

    if 0 <= confidence <= 1:
        confidence *= 100

    if not 0 <= confidence <= 100:
        return jsonify({"error": "Invalid confidence"}), 400

    with get_db() as db:
        user = db.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user is None:
            return jsonify({"error": "User not found"}), 404

        db.execute("""
            INSERT INTO analyses (user_id, result, confidence)
            VALUES (?, ?, ?)
        """, (user["id"], result, confidence))

        db.commit()

    return jsonify({
        "received": True,
        "class": result,
        "confidence": confidence
    }), 200
    
       if __name__ == "__main__":
          port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
