import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_file
import threading
import yt_dlp

app = Flask(__name__)

download_completed = False
downloaded_videos = {}  
playlist_name = ""  # To store playlist folder name if it's a playlist


def download_playlist(playlist_url, save_path):

    global download_completed, downloaded_videos, playlist_name

    ydl_opts = {
        'outtmpl': f"{save_path}/%(playlist_title)s/%(title)s.%(ext)s",
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=True)

        if 'entries' in info_dict:  
            playlist_name = info_dict.get('title', 'Downloaded_Playlist')
            playlist_path = os.path.join(save_path, playlist_name)

            for entry in info_dict['entries']:
                if entry:
                    title = entry.get('title', 'unknown')
                    ext = entry.get('ext', 'mp4')
                    downloaded_videos[title] = ext
        else:  
            playlist_name = ""
            title = info_dict.get('title', 'unknown')
            ext = info_dict.get('ext', 'mp4')
            downloaded_videos[title] = ext

    download_completed = True


@app.route('/')
def home_page():
    return render_template('Home_Page.html')


@app.route('/', methods=['POST'])
def get_value():
    global download_completed
    download_completed = False

    playlist_url = request.form['url_value']
    
    if not playlist_url:
        return render_template('Terminated_Page.html')

    save_path = "Downloads/"
    thread = threading.Thread(target=download_playlist, args=(playlist_url, save_path))
    thread.start()

    return render_template('Procedure_Page.html')


@app.route('/check_status')
def check_status():
    global download_completed
    if download_completed:
        return redirect(url_for('success_page'))
    return '', 204  # No content yet


@app.route('/success')
def success_page():
    if playlist_name:
        path = f"Downloads/{playlist_name}"
        return render_template('Successful_Page.html', path=path, title=playlist_name, ext="zip")
    else:
        title, ext = list(downloaded_videos.items())[0]
        path = f"Downloads/{title}.{ext}"
        return render_template('Successful_Page.html', path=path, title=title, ext=ext)


@app.route('/file')
def file_download():
    if playlist_name:
        zip_path = f"Downloads/{playlist_name}.zip"

        # Zip the playlist folder if not already zipped
        if not os.path.exists(zip_path):
            shutil.make_archive(zip_path.replace('.zip', ''), 'zip', f"Downloads/{playlist_name}")

        return send_file(zip_path, as_attachment=True)
    else:
        title, ext = list(downloaded_videos.items())[0]
        path = f"Downloads/{title}.{ext}"
        return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
