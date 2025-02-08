from flask import Flask, render_template, request , redirect , url_for
import threading
import yt_dlp

app = Flask(__name__)

download_completed = False


def download_playlist(playlist_url, save_path):
    global download_completed

    ydl_opts = {
        'outtmpl': f"{save_path}/%(title)s.%(ext)s",
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

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

    save_path = r"D:\AMAN"

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
    return render_template('Successful_Page.html')


if __name__ == '__main__':
    app.run(debug=True)
