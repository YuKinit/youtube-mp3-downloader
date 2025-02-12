from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

# Ensure the downloads folder exists
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form["url"]
        try:
            yt = YouTube(youtube_url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            file_path = audio_stream.download(DOWNLOAD_FOLDER)

            # Convert to MP3
            base, ext = os.path.splitext(file_path)
            mp3_file = base + ".mp3"
            os.rename(file_path, mp3_file)

            return send_file(mp3_file, as_attachment=True)
        except Exception as e:
            return f"Error: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
