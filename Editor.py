import requests
import random
import os
import mimetypes
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeAudioClip, CompositeVideoClip, concatenate_videoclips
from string import ascii_letters, digits
chars = ascii_letters + digits


class Editor:
    def download(self, url: str, path):
        res = requests.get(url, stream=True)
        content_type = res.headers["content-type"]
        video_id = ''.join(random.choice(chars) for i in range(10))
        self.video_id = video_id
        self.file_ext = mimetypes.guess_extension(content_type)
        with open(f"{path}/{video_id}{self.file_ext}", "wb") as f:
            for chunk in res.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
            f.close()

    def prepareForEditing(self, url):
        self.download(url, "tmp/")
        path = f"tmp/{self.video_id}{self.file_ext}"
        video = VideoFileClip(path)
        size = video.size
        indexMax = size.index(max(size))
        indexMin = size.index(min(size))
        diff = size[indexMax] - size[indexMin]
        half = int(diff/2)
        if diff > 0 and indexMax == 0:
            clip: VideoClip = video.margin(top=half, bottom=half)
            clip: VideoClip = clip.resize((720, 720))
        elif diff > 0 and indexMax == 1:
            clip: VideoClip = video.margin(left=half, right=half)
            clip: VideoClip = clip.resize((720, 720))
        else:
            clip: VideoClip = video.resize((720, 720))
        return clip

    def curb_your_enthusiasm(self, url, duration):
        clip = self.prepareForEditing(url)
        video_id = self.video_id
        file_ext = self.file_ext
        outro_video = VideoFileClip("assets/video/curb_your_enthusiasm.mp4").resize((720, 720))
        outro_audio = AudioFileClip("assets/audio/curb_your_enthusiasm.mp3")
        duration = int(float(duration))
        audio = CompositeAudioClip(
            [clip.audio.set_end(duration), outro_audio.set_start(int(duration - duration * 0.15))])
        final = concatenate_videoclips(
            [clip.set_end(duration), outro_video], method="compose").set_end(audio.duration).set_audio(audio)
        final.write_videofile(f"out/{video_id}.mp4", fps=30,
                              logger=None, temp_audiofile=f"tmp/{video_id}.mp3")
        clip.close()
        final.close()
        os.remove(f"tmp/{video_id}{file_ext}")

    def average(self, text: list):
        template = VideoFileClip("assets/video/average.mp4")
        text_1 = TextClip(text[0], font="segoe-ui", fontsize=25).set_position(
            (120, 45)).set_duration(template.duration)
        text_2 = TextClip(text[1], font="segoe-ui", fontsize=25).set_position(
            (480, 45)).set_duration(template.duration)
        final = CompositeVideoClip([template, text_1])
        final = CompositeVideoClip([final, text_2])
        self.video_id = ''.join(random.choice(chars) for i in range(10))
        final.write_videofile(f"out/{self.video_id}.mp4", fps=30,
                              logger=None, temp_audiofile=f"tmp/{self.video_id}.mp3")
