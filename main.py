#youtube transcript

from youtube_transcript_api import YouTubeTranscriptApi


video_id = 'Ydts27Qa8H0'
ytt_api = YouTubeTranscriptApi()
fetched_transcript = ytt_api.fetch(video_id)

for snippet in fetched_transcript:
    print(snippet.text)