from flask import Flask, render_template, g, url_for, redirect, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DATABASE = os.path.join(app.root_path, "Databases/tables.db")

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

# Routes
@app.route('/')
@app.route('/index.html')
@app.route('/explore.html')
@app.route('/search.html')
@app.route('/login.html')
def index():
    db = get_db()
    cur = db.execute("SELECT * FROM games")
    rows = cur.fetchall()
    games = [dict(r) for r in rows]
    return render_template('index.html', games=games)

@app.route("/like/<int:game_id>")
def like_game(game_id):
    print(f"User liked {game_id}")
    return redirect(url_for("index"))

@app.route("/details/<int:game_id>")
def details(game_id):
    db = get_db()
    cur = db.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
    row = cur.fetchone()
    if row:
        return render_template("details.html", game=dict(row))
    return "Game not found", 404

@app.route("/play/<int:game_id>")
def play_game(game_id):
    db = get_db()
    cur = db.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
    row = cur.fetchone()
    if row:
        game = dict(row)
        # Add your game playing logic here
        return f"Now playing: {game['name']}"
    return "Game not found", 404

@app.route("/add_to_cart/<int:game_id>")
def add_to_cart(game_id):
    db = get_db()
    cur = db.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
    row = cur.fetchone()
    if row:
        game = dict(row)
        # Add your cart logic here
        return f"Added {game['name']} to cart"
    return "Game not found", 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


app = Flask(__name__)
app.secret_key = "abcdefg" 
app.permanent_session_lifetime = timedelta(days=7)

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# User authentication functions
def get_user_by_username(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(username, email, password):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (username, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Routes
@app.route('/')
def index():
    if "user" in session:
        return render_template('index.html', username=session["user"])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        
        if user and user[3] == password:  # Simple password check (not secure)
            session.permanent = True
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "error")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('login.html')
        
        if add_user(username, email, password):
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        else:
            flash("Username or email already exists", "error")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("You have been logged out", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)