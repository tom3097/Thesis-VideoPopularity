from video_popularity import app
from flask import render_template, url_for


@app.route('/')
def index():
    return render_template('index.html')
