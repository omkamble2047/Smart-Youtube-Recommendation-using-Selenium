import streamlit as st
from id import get_youtube_video_ids_selenium


st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.wallpaperscraft.com/image/single/solid_colors_stains_18571_300x168.jpg");
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
    for i in ids:
        st.write(f'https://www.youtube.com/watch?v={i}')
        st.video(f'https://www.youtube.com/watch?v={i}')
