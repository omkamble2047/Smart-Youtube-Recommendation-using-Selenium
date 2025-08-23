import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from id import get_youtube_video_ids_selenium

# 🔹 Configure Gemini
genai.configure(api_key="AIzaSyDLUbjBIrAd95Mgz38D9HjpaK_VbZyXVS0")  
model = genai.GenerativeModel("gemini-1.5-flash")


def fetch_transcripts(query: str, max_videos=5):
    """
    Fetch transcripts for top YouTube search results of a query.
    Returns a dictionary {video_id: transcript_text}.
    """
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+').lower()}&sp=EgIIBA%253D%253D"
    ids = get_youtube_video_ids_selenium(url)[:max_videos]

    transcripts = {}
    for vid in ids:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid, languages=['en', 'hi'])
            text = " ".join([t['text'] for t in transcript])
            transcripts[vid] = text
        except Exception as e:
            transcripts[vid] = f"Transcript not available ({e})"
    return transcripts


def summarize_and_rank(transcripts: dict):
    """
    Sends transcripts to Gemini, gets summaries, and ranks them by clarity.
    Returns a list of dicts sorted by clarity.
    """
    summaries = []

    for vid, text in transcripts.items():
        if "Transcript not available" in text:
            summaries.append({
                "video_id": vid,
                "summary": "Transcript not available",
                "clarity_score": 0
            })
            continue

        prompt = f"""
        I have a transcript of a YouTube video. Please:
        1. Summarize it clearly in 5-6 sentences.
        2. Rate how easy it is to understand on a scale of 1 to 10 (10 = very clear for beginners).
        
        Transcript:
        {text[:6000]}  # trimming to avoid token limits
        """

        response = model.generate_content(prompt)
        result = response.text

        # Try to extract a clarity score if Gemini provides one
        clarity_score = 5
        for word in result.split():
            if word.isdigit() and 1 <= int(word) <= 10:
                clarity_score = int(word)
                break

        summaries.append({
            "video_id": vid,
            "summary": result,
            "clarity_score": clarity_score
        })

    # Sort by clarity (highest first)
    return sorted(summaries, key=lambda x: x['clarity_score'], reverse=True)


if __name__ == "__main__":
    query = "machine learning basics"
    transcripts = fetch_transcripts(query)
    ranked_summaries = summarize_and_rank(transcripts)

    for idx, item in enumerate(ranked_summaries, start=1):
        print(f"\nRank {idx} | Video: https://www.youtube.com/watch?v={item['video_id']}")
        print(f"Clarity Score: {item['clarity_score']}")
        print(f"Summary: {item['summary']}\n")
