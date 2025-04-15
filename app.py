from fastapi import FastAPI, HTTPException
import yt_dlp
from pyrogram import Client, errors
import asyncio

# Initialize FastAPI
app = FastAPI()

# Set up Pyrogram Client with session string
SESSION_STRING = "BQG3YngAJjfV40-kgdRRoOU75riZyE2bMB5vXUXLMNr88AKpGAIO6sP73tJHI8xNEaW1so797OSrqdAIPGqlEllLWak5dxI6uFn5Xd-ttHcb7Gbhb_JGBf1imEYqUHQmAZPFrdogiQzPm9UMv7cE48qtl-Sd552VVeiKbaQy_HN6cXNy9ady-MwQ2p05KOjr4fl0u7SpTWHLGji4g0fTgf1YGu4h4YpJrjQjiS9axfTnODK3_8rnwK0hsAuVtHxiNqf95Oxb_8xBm0CPjZWmBuEk2vjyJODcQzpEQ4hpQkpM-GDmDEPxbOgJrIkZ_YODWfQC6-6-peIoxiIBUZR9clOUGhDkjgAAAAGz8DqsAA"

# Create Pyrogram client
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
    try:
        # Ensure the Pyrogram client is connected only once
        if not app_client.is_connected:
            await app_client.start()  # Start the client if not connected

        video_url = download_video_with_session(url)
        
        if video_url:
            return {"download_url": video_url}
        else:
            raise HTTPException(status_code=400, detail="Video not found or error occurred.")
    
    except errors.FloodWait as e:
        # Handle the case where Pyrogram throws flood wait error
        raise HTTPException(status_code=429, detail=f"Flood wait: {e.x} seconds.")
    
    except Exception as e:
        # General exception handler
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    finally:
        # Close the Pyrogram client after the request
        if app_client.is_connected:
            await app_client.stop()
