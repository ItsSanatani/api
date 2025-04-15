from fastapi import FastAPI, HTTPException
import yt_dlp
from pyrogram import Client
import asyncio

# Initialize FastAPI
app = FastAPI()

# Set up Pyrogram Client with session string
SESSION_STRING = "BQG3YngAJjfV40-kgdRRoOU75riZyE2bMB5vXUXLMNr88AKpGAIO6sP73tJHI8xNEaW1so797OSrqdAIPGqlEllLWak5dxI6uFn5Xd-ttHcb7Gbhb_JGBf1imEYqUHQmAZPFrdogiQzPm9UMv7cE48qtl-Sd552VVeiKbaQy_HN6cXNy9ady-MwQ2p05KOjr4fl0u7SpTWHLGji4g0fTgf1YGu4h4YpJrjQjiS9axfTnODK3_8rnwK0hsAuVtHxiNqf95Oxb_8xBm0CPjZWmBuEk2vjyJODcQzpEQ4hpQkpM-GDmDEPxbOgJrIkZ_YODWfQC6-6-peIoxiIBUZR9clOUGhDkjgAAAAGz8DqsAA"

# Set up Pyrogram Client
app_client = Client("my_session", session_string=SESSION_STRING)

# yt-dlp function for downloading video/audio with session
def download_video_with_session(url: str):
    try:
        # Set up yt-dlp options with session (cookies)
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Best quality video and audio
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Output file template
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get("url", None)
            if video_url:
                return video_url  # return the URL of the video or audio stream

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.get("/api")
async def download_video(url: str):
    # Ensure the Pyrogram client is initialized correctly and authenticate session
    await app_client.start()  # Starts the Pyrogram client to use session
    try:
        # Now call yt-dlp to fetch video/audio URL
        video_url = download_video_with_session(url)
        if video_url:
            return {"download_url": video_url}
        else:
            raise HTTPException(status_code=400, detail="Video not found or error occurred.")
    finally:
        await app_client.stop()  # Ensure we stop the Pyrogram client after the request
