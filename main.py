from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "abcdef"

DATABASE = "Databases/tables.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_games(limit=None, order_by="release_date DESC"):
    conn = get_db_connection()
    query = "SELECT * FROM games ORDER BY " + order_by
    if limit:
        query += f" LIMIT {limit}"
    games_list = conn.execute(query).fetchall()
    conn.close()
    return games_list

@app.route("/")
def home():
    recommended_games = fetch_games(limit=4)
    new_games = fetch_games(limit=4, order_by="release_date DESC")
    trending_games = fetch_games(limit=4, order_by="views DESC")
    return render_template(
        "partials/menu.html",
        recommended_games=recommended_games,
        new_games=new_games,
        trending_games=trending_games,
        session=session
    )

@app.route("/games/recommended")
def recommended_games():
    games = fetch_games()
    return render_template("games_list.html", title="Recommended Games", games=games)

@app.route("/games/new")
def new_games():
    games = fetch_games(order_by="release_date DESC")
    return render_template("games_list.html", title="New Releases", games=games)

@app.route("/games/trending")
def trending_games():
    games = fetch_games()
    return render_template("games_list.html", title="Trending Games", games=games)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not username or not email or not password:
            flash("All fields are required", "danger")
            return render_template("signup.html")
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (username, email, hashed_password, datetime.now())
            )
            conn.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists", "danger")
        finally:
            conn.close()
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You’ve been logged out.", "info")
    return redirect(url_for("home"))

@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please login to view your profile.", "warning")
        return redirect(url_for("login"))
    return render_template("profile.html", username=session["username"])

@app.route("/explore")
def explore():
    return render_template("explore.html", title="Explore")

@app.route("/games")
def games():
    games = fetch_games()
    return render_template("games_list.html", title="All Games", games=games)

@app.route("/games/<int:game_id>")
def game_detail(game_id):
    conn = get_db_connection()
    game = conn.execute("SELECT * FROM games WHERE game_id = ?", (game_id,)).fetchone()
    conn.close()
    if not game:
        return "<h1>Game not found</h1>", 404
    return render_template("game_detail.html", game=game)

if __name__ == "__main__":
    app.run(debug=True)
