from flask import Flask, request, redirect, session, render_template
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "atslega"  

DB_NAME = "colorgenlogin.db"


def get_db():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


init_db()


@app.route("/")
def home():
    if "user" in session:
        return render_template("home.html", user=session['user'])
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with get_db() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user"] = email
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid email or password")
    
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]

    hashed_password = generate_password_hash(password)

    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (email, password, created_at) VALUES (?, ?, ?)",
                (email, hashed_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
        return render_template("login.html", success="Registration successful! Please login.")
    except sqlite3.IntegrityError:
        return render_template("login.html", error="Email already exists!")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
