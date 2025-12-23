from flask import Flask, request, send_file
import subprocess
import requests
import uuid
import os

app = Flask(__name__)

@app.route("/render", methods=["POST"])
def render_video():
    data = request.json

    image_url = data["image_url"]
    audio_url = data["audio_url"]
    text = data["text"]

    img = f"/tmp/{uuid.uuid4()}.jpg"
    aud = f"/tmp/{uuid.uuid4()}.mp3"
    out = f"/tmp/{uuid.uuid4()}.mp4"

    open(img, "wb").write(requests.get(image_url).content)
    open(aud, "wb").write(requests.get(audio_url).content)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "5", "-i", img,
        "-i", aud,
        "-vf",
        f"drawtext=text='{text}':fontcolor=white:fontsize=72:"
        "box=1:boxcolor=black@0.6:boxborderw=12:"
        "x=(w-text_w)/2:y=h-240",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        out
    ]

    subprocess.run(cmd, check=True)

    return send_file(out, mimetype="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

