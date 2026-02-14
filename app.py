from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "emotionconnectsecret"

# In-memory storage
chat_rooms = {
    "stressed": [],
    "anxious": [],
    "happy": [],
    "motivated": []
}
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

def generate_username():
    return "User" + str(random.randint(100, 999))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/emotions')
def emotions():
    return render_template("emotions.html")

@app.route('/chat/<emotion>', methods=['GET', 'POST'])
def chat(emotion):

    if emotion not in chat_rooms:
        return "Invalid emotion", 404

    if "username" not in session:
        session["username"] = generate_username()

    username = session["username"]

    if request.method == "POST":
        message = request.form.get("message")
        if message:
            chat_rooms[emotion].append((username, message))
        return redirect(f"/chat/{emotion}")

    messages = chat_rooms[emotion]

    return render_template("chat.html", emotion=emotion, messages=messages, username=username)

if __name__ == "__main__":
    app.run(debug=True)
init_db()
