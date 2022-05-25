import os
from Editor import Editor
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
app = FastAPI()


@app.get("/curb_your_enthusiasm", response_class=ORJSONResponse)
def render(url, duration: float):
    editor = Editor()
    editor.curb_your_enthusiasm(url, duration)
    return {"path": os.path.abspath(f"out/{editor.video_id}.mp4")}
