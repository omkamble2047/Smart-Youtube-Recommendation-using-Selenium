# import streamlit as st
from id import get_youtube_video_ids_selenium
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()


from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create database if not exists
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
                return redirect('/dashboard')
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

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-image: url("https://sjunkins.wordpress.com/wp-content/uploads/2012/04/the-best-top-desktop-hd-dark-black-wallpapers-dark-black-wallpaper-dark-background-dark-wallpaper-23.jpg?w=900");
#         background-size: cover;
#         background-repeat: no-repeat;
#         background-attachment: fixed;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Streamlit UI
# st.header('Smart YouTube Recommendation')

# labels = st.text_input("Enter the topics to receive best recommendations")
# labels = labels.replace(' ','+').lower()
# button = st.button("Submit")

# url = f"https://www.youtube.com/results?search_query={labels}&sp=EgIIBA%253D%253D"

# if button:
#     st.markdown(url)
#     ids = get_youtube_video_ids_selenium(url)
#     # st.write(ids)
#     d = {}
#     # ls = []
#     for i in ids:
#         ls = []
#         video_link = f'https://www.youtube.com/watch?v={i}'
#         fetched_transcript = ytt_api.fetch(i,  languages=['hi', 'en'])
#         for snippet in fetched_transcript:
#             # st.markdown(snippet.text)
#             ls.append(snippet.text)
#         d[i] = ls
#         st.write(d)
#         st.write(video_link)
#         st.video(video_link)
#     # print(d)
