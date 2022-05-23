import requests
import numpy as np
import random
import os
import mimetypes
from moviepy.editor import *
from string import ascii_letters, digits
chars = ascii_letters + digits


class Editor:
    def download(self, url: str, name):
        res = requests.get(url, stream=True)
        content_type = res.headers["content-type"]
        file_ext = mimetypes.guess_extension(content_type)
        video_name = f"{name}{file_ext}"
        with open(video_name, "wb") as f:
            for chunk in res.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
            f.close()
        return video_name

    def prepareForEditing(self, url):
        video_id = ''.join(random.choice(chars) for i in range(10))
        video_name = self.download(url, f"tmp/{video_id}")
        video = VideoFileClip(video_name)
        size = video.size
        indexMax = size.index(max(size))
        indexMin = size.index(min(size))
        diff = size[indexMax] - size[indexMin]
        half = int(diff/2)
        if indexMax == 0:
            clip: VideoClip = video.margin(top=half, bottom=half)
        else:
            clip: VideoClip = video.margin(left=half, right=half)
        return {"clip": clip, "id": video_id}
