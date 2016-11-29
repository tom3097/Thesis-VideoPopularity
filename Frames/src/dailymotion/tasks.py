__author__ = "Tomasz Bochenski"

from celery import Celery
from os import path, makedirs
from subprocess import call
from youtube_dl import YoutubeDL

app = Celery('tasks', backend='redis://', broker='amqp://')

@app.task
def download_frames(video_id, result_path):
    video_name = '{}.mp4'.format(video_id)
    ydl_opt = {
        'quiet': True,
        'format': 'mp4',
        'outtmpl': '%(id)s.%(ext)s'
    }
    downloader = YoutubeDL(ydl_opt)
    video_path = 'http://www.dailymotion.com/video/{}'.format(video_id)
    try:
        downloader.download([video_path])
        if not path.exists(path.join(result_path, video_id)):
            makedirs(path.join(result_path, video_id))
        frame_names = path.join(result_path, video_id, '{}_%d.jpg'.format(video_id))
        frame_proc = call('ffmpeg -i "{}" -an -sn -vsync 0 -vf select="not(mod(n\,8))" -t 6 "{}"'.format(video_name, frame_names), shell=True)
    finally:
        rm_proc = call('rm -- ./{}*'.format(video_name), shell=True)
    return video_id

