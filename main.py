from Editor import Editor
from moviepy.editor import *
from fastapi import FastAPI

app = FastAPI()


@app.get("/curb_your_enthusiasm")
def render(url):
    res = Editor().prepareForEditing(url)
    clip = res["clip"]
    video_id = res["id"]
    clip.write_videofile(f"out/{video_id}_out.mp4", codec="mpeg4")
