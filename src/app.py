from flask import Flask, render_template, request, redirect, session, flash
import sqlite3, os
from youtube_transcript_api import YouTubeTranscriptApi
from id import get_youtube_video_ids_selenium
import google.generativeai as genai

# Flask setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Gemini setup
genai.configure(api_key="AIzaSyCOjTarmwkiG8BlrmaRZh7K5VuV5xQOFG4")  
model = genai.GenerativeModel("gemini-1.5-flash")


# Create DB if not exists
def init_db():
    if not os.path.exists('users.db'):
        with sqlite3.connect('users.db') as conn:
            conn.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                );
            ''')


@app.route('/')
def home():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()
            if user:
                session['username'] = username
                return redirect('/learn')
            else:
                flash("Invalid login")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect('users.db') as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                flash("Signup successful. Please login.")
                return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Username already exists")
    return render_template('signup.html')

@app.route('/learn', methods=['GET', 'POST'])
def lear():
    if 'username' not in session:
        return redirect('/login')

    summaries = []
    if request.method == 'POST':
        topic = request.form['topic']
        url = f"https://www.youtube.com/results?search_query={topic.replace(' ', '+').lower()}&sp=EgIIBA%253D%253D"
        ids = get_youtube_video_ids_selenium(url)[:5]  # Limit to top 5

        for vid in ids:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(vid, languages=['en', 'hi'])
                text = " ".join([t['text'] for t in transcript])
            except Exception as e:
                text = f"Transcript not available ({e})"

            prompt = f"""
            Summariztion Of The Video Is Not Possible As Video Has No Captions!

            Transcript:
            {text[:6000]}
            """

            response = model.generate_content(prompt)
            summary_text = response.text

            # Extract clarity score
            clarity_score = 5
            for word in summary_text.split():
                if word.isdigit() and 1 <= int(word) <= 10:
                    clarity_score = int(word)
                    break

            summaries.append({
                "video_id": vid,
                "link": f"https://www.youtube.com/watch?v={vid}",
                "summary": summary_text,
                "clarity_score": clarity_score
            })

        # Sort by clarity (highest first)
        summaries = sorted(summaries, key=lambda x: x['clarity_score'], reverse=True)

    return render_template('learn.html', user=session['username'], summaries=summaries)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
