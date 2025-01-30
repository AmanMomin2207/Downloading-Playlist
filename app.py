from flask import Flask , render_template , request , redirect , url_for , jsonify
import threading
import time
import yt_dlp

app = Flask(__name__)


@app.route('/')
def Home_Page():
    return render_template('Home_Page.html')

@app.route('/', methods=['POST'])
def getvalue():
    playlist_url = request.form['url_value']

    if(playlist_url == ""):
        return render_template('Terminated_Page.html')
    

    save_path = r"D:\AMAN"

    ydl_opts = {
        'outtmpl': f"{save_path}/%(title)s.%(ext)s",  # Output file naming
        'format': 'bestvideo+bestaudio/best',        # Best video and audio streams
        'merge_output_format': 'mp4',               # Merge into .mp4 file
        'ignoreerrors': True,                       # Skip errors
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])


if __name__ == '__main__':
    app.run(debug=True)