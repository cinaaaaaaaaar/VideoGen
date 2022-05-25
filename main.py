import os
from Editor import Editor
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
app = FastAPI()


@app.get("/curb_your_enthusiasm", response_class=ORJSONResponse)
def render(url, duration: float):
    editor = Editor()
    clip = editor.prepareForEditing(url)
    video_id = editor.video_id
    file_ext = editor.file_ext
    outro_video = VideoFileClip("assets/video/curb_your_enthusiasm.mp4").resize((720, 720))
    outro_audio = AudioFileClip("assets/audio/curb_your_enthusiasm.mp3")
    duration = int(duration)
    audio = CompositeAudioClip(
        [clip.audio.set_end(duration), outro_audio.set_start(int(duration - duration * 0.15))])
    final = concatenate_videoclips(
        [clip.set_end(duration), outro_video], method="compose").set_end(audio.duration).set_audio(audio)
    final.write_videofile(f"out/{video_id}.mp4", fps=30,
                          logger=None, temp_audiofile=f"tmp/{video_id}.mp3")
    clip.close()
    final.close()
    os.remove(f"tmp/{video_id}{file_ext}")
    return {"path": os.path.abspath(f"out/{video_id}.mp4")}
