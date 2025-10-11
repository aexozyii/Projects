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

def add_comment(user_id, game_id, content):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO comments (user_id, game_id, content) VALUES (?, ?, ?)",
        (user_id, game_id, content)
    )
    conn.commit()
    conn.close()

def get_comments_for_game(game_id):
    conn = get_db_connection()
    comments = conn.execute("""
        SELECT c.content, c.created_at, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.user_id
        WHERE c.game_id = ?
        ORDER BY c.created_at DESC
    """, (game_id,)).fetchall()
    conn.close()
    return comments

def fetch_games(query=None, genre_id=None, limit=None, order_by=None):
    conn = get_db_connection()
    sql = """
        SELECT g.*, GROUP_CONCAT(gen.name, ', ') as genres
        FROM games g
        LEFT JOIN game_genres gg ON g.game_id = gg.game_id
        LEFT JOIN genres gen ON gg.genre_id = gen.genre_id
    """
    params = []
    where_clauses = []
    if query:
        like_query = f"%{query}%"
        where_clauses.append("(g.title LIKE ? OR g.description LIKE ? OR g.developer LIKE ? OR g.publisher LIKE ?)")
        params.extend([like_query, like_query, like_query, like_query])
    if genre_id:
        where_clauses.append("gg.genre_id = ?")
        params.append(genre_id)
    if where_clauses:
        sql += " WHERE " + " AND ".join(where_clauses)
    sql += " GROUP BY g.game_id"
    if order_by:
        sql += f" ORDER BY {order_by}"
    if limit:
        sql += f" LIMIT {limit}"
    games_list = conn.execute(sql, tuple(params)).fetchall()
    conn.close()
    return games_list


@app.route("/games/genre/<int:genre_id>")
def games_by_genre(genre_id):
    games_list = fetch_games(genre_id=genre_id)
    conn = get_db_connection()
    genre = conn.execute("SELECT * FROM genres WHERE genre_id = ?", (genre_id,)).fetchone()
    conn.close()
    return render_template("games_list.html", title=f"Genre: {genre['name']}", games=games_list)

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
    conn = get_db_connection()
    games = conn.execute("SELECT * FROM games").fetchall()
    conn.close()
    return render_template(
        "games_list.html",
        recommended_games="Recommended Games",
        games=games
    )

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
    conn = get_db_connection()
    favorites = conn.execute("""
        SELECT g.game_id, g.title, g.cover_image_url
        FROM favorites f
        JOIN games g ON f.game_id = g.game_id
        WHERE f.user_id = ?
    """, (session["user_id"],)).fetchall()
    last_visited = conn.execute("""
        SELECT g.game_id, g.title, g.cover_image_url, lv.visited_at
        FROM last_visited lv
        JOIN games g ON lv.game_id = g.game_id
        WHERE lv.user_id = ?
        GROUP BY g.game_id
        ORDER BY lv.visited_at DESC
        LIMIT 5
    """, (session["user_id"],)).fetchall()
    conn.close()
    return render_template(
        "profile.html",
        username=session["username"],
        favorites=favorites,
        last_visited=last_visited
    )

@app.route("/about")
def about():
    return render_template("about_page.html")

@app.route("/games")
def games():
    query = request.args.get("query")
    if query == "":
        query =""
    games_list = fetch_games(query)
    return render_template("games_list.html", title="Search Results", games=games_list, query=query)

@app.route("/games/<int:game_id>", methods=["GET", "POST"])
def game_detail(game_id):
    conn = get_db_connection()
    game = conn.execute("SELECT * FROM games WHERE game_id = ?", (game_id,)).fetchone()
    if not game:
        conn.close()
        return "<h1>Game not found</h1>", 404
    genres = conn.execute("""
        SELECT g.genre_id, g.name
        FROM genres g
        JOIN game_genres gg ON g.genre_id = gg.genre_id
        WHERE gg.game_id = ?
    """, (game_id,)).fetchall()
    is_favorite = False
    if "user_id" in session:
        is_favorite = conn.execute("""
            SELECT 1 FROM favorites WHERE user_id = ? AND game_id = ?
        """, (session["user_id"], game_id)).fetchone() is not None
        conn.execute("""
            DELETE FROM last_visited WHERE user_id = ? AND game_id = ?
        """, (session["user_id"], game_id))
        conn.execute("""
            INSERT INTO last_visited (user_id, game_id, visited_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (session["user_id"], game_id))
        conn.commit()
        if request.method == "POST":
            comment = request.form.get("comment")
            if comment:
                add_comment(session["user_id"], game_id, comment)
                flash("Comment posted!", "success")
                return redirect(url_for("game_detail", game_id=game_id))
    comments = get_comments_for_game(game_id)
    conn.close()
    return render_template(
        "game_detail.html",
        game=game,
        genres=genres,
        is_favorite=is_favorite,
        comments=comments
    )

@app.route("/game/<int:game_id>/favorite", methods=["POST"])
def toggle_favorite(game_id):
    if "user_id" not in session:
        flash("You must be logged in to favorite games.", "warning")
        return redirect(url_for("login"))
    user_id = session["user_id"]
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT * FROM favorites WHERE user_id = ? AND game_id = ?",
        (user_id, game_id)
    ).fetchone()
    if existing:
        conn.execute(
            "DELETE FROM favorites WHERE user_id = ? AND game_id = ?",
            (user_id, game_id)
        )
        flash("Removed from favorites.", "info")
    else:
        # Add to favorites
        conn.execute(
            "INSERT INTO favorites (user_id, game_id) VALUES (?, ?)",
            (user_id, game_id)
        )
        flash("Added to favorites!", "success")
    conn.commit()
    conn.close()
    return redirect(url_for("game_detail", game_id=game_id))

conn = get_db_connection()
genres = conn.execute("SELECT * FROM game_genres").fetchall()
conn.close()

if __name__ == "__main__":
    app.run(debug=True)
