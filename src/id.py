from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time



def get_youtube_video_ids_selenium(query_url, max_videos=10):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    driver.get(query_url)
    time.sleep(5)  # wait for page to load

    content = driver.page_source
    matches = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', content)

    video_ids = []
    seen = set()
    for vid in matches:
        if vid not in seen:
            video_ids.append(vid)
            seen.add(vid)
        if len(video_ids) >= max_videos:
            break

    driver.quit()
    return video_ids