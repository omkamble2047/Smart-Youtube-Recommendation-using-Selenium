import streamlit as st
from id import get_youtube_video_ids_selenium
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://sjunkins.wordpress.com/wp-content/uploads/2012/04/the-best-top-desktop-hd-dark-black-wallpapers-dark-black-wallpaper-dark-background-dark-wallpaper-23.jpg?w=900");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.header('Smart YouTube Recommendation')

labels = st.text_input("Enter the topics to receive best recommendations")
labels = labels.replace(' ','+').lower()
button = st.button("Submit")

url = f"https://www.youtube.com/results?search_query={labels}&sp=EgIIBA%253D%253D"

if button:
    st.markdown(url)
    ids = get_youtube_video_ids_selenium(url)
    # st.write(ids)
    d = {}
    # ls = []
    for i in ids:
        ls = []
        video_link = f'https://www.youtube.com/watch?v={i}'
        fetched_transcript = ytt_api.fetch(i,  languages=['hi', 'en'])
        for snippet in fetched_transcript:
            # st.markdown(snippet.text)
            ls.append(snippet.text)
        d[i] = ls
        st.write(d)
        st.write(video_link)
        st.video(video_link)
    # print(d)
