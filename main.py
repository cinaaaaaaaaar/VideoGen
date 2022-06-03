import os
from Editor import Editor
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse


app = FastAPI()


@app.post("/curb_your_enthusiasm/")
async def render(req: Request):
    data = req.headers
    url = data.get("url")
    duration = data.get("duration")
    editor = Editor()
    editor.curb_your_enthusiasm(url, duration)
    return {"path": os.path.abspath(f"out/{editor.video_id}.mp4")}


@app.post("/average/")
async def render(req: Request):
    editor = Editor()
    data = req.headers
    text = [data.get("text1"), data.get("text2")]
    editor.average(text)
    return {"path": os.path.abspath(f"out/{editor.video_id}.mp4")}
