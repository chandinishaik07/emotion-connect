from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "emotionconnectsecret"

def generate_username():
    return "User" + str(random.randint(100, 999))

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emotion TEXT,
            username TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/emotions')
def emotions():
    return render_template("emotions.html")

@app.route('/chat/<emotion>', methods=['GET', 'POST'])
def chat(emotion):

    if "username" not in session:
        session["username"] = generate_username()

    username = session["username"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        message = request.form.get("message")

        if message:
            cursor.execute(
                "INSERT INTO messages (emotion, username, message) VALUES (?, ?, ?)",
                (emotion, username, message)
            )
            conn.commit()

        conn.close()
        return redirect(f"/chat/{emotion}")

    cursor.execute("SELECT * FROM messages WHERE emotion = ?", (emotion,))
    messages = cursor.fetchall()
    conn.close()

    return render_template("chat.html", emotion=emotion, messages=messages, username=username)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
