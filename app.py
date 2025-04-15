from fastapi import FastAPI, HTTPException
import yt_dlp
from pyrogram import Client

app = FastAPI()

SESSION_STRING = "BQG3YngAJjfV40-kgdRRoOU75riZyE2bMB5vXUXLMNr88AKpGAIO6sP73tJHI8xNEaW1so797OSrqdAIPGqlEllLWak5dxI6uFn5Xd-ttHcb7Gbhb_JGBf1imEYqUHQmAZPFrdogiQzPm9UMv7cE48qtl-Sd552VVeiKbaQy_HN6cXNy9ady-MwQ2p05KOjr4fl0u7SpTWHLGji4g0fTgf1YGu4h4YpJrjQjiS9axfTnODK3_8rnwK0hsAuVtHxiNqf95Oxb_8xBm0CPjZWmBuEk2vjyJODcQzpEQ4hpQkpM-GDmDEPxbOgJrIkZ_YODWfQC6-6-peIoxiIBUZR9clOUGhDkjgAAAAGz8DqsAA"

app_client = Client("my_session", session_string=SESSION_STRING)

def download_video_with_session(url: str):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from {url}")  # Debugging line
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get("url", None)
            if video_url:
                return video_url
            else:
                raise Exception("Video URL extraction failed")

    except Exception as e:
        print(f"Error during video extraction: {str(e)}")  # Log error
        raise HTTPException(status_code=400, detail=f"Error during video extraction: {str(e)}")

@app.get("/api")
async def download_video(url: str):
    try:
        await app_client.start()
        print(f"Fetching video for URL: {url}")  # Debugging line
        video_url = download_video_with_session(url)
        if video_url:
            return {"download_url": video_url}
        else:
            raise HTTPException(status_code=400, detail="Video not found or error occurred.")
    except Exception as e:
        print(f"Internal error: {str(e)}")  # Log internal error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        await app_client.stop()
