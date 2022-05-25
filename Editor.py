import requests
import numpy as np
import random
import os
import mimetypes
from moviepy.editor import VideoFileClip
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
            clip.resize((720, 720))
        elif diff > 0 and indexMax == 1:
            clip: VideoClip = video.margin(left=half, right=half)
            clip.resize((720, 720))
        else:
            clip = video.resize((720, 720))
        return clip
