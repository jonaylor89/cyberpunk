
from pydub import AudioSegment

from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/audio/<filename>")
def stream_mp3(filename: str):
    def generate():
        with open(f"testdata/{filename}.mp3", "rb") as fmp3:
            data = fmp3.read(1024)
            while data:
                yield data
                data = fmp3.read(1024)

    return Response(generate(), mimetype="audio/mp3")

@app.route("/reverse/<filename>")
def stream_reverse(filename: str):
    song = AudioSegment.from_mp3(f"testdata/{filename}.mp3")
    reversed_song = song.reverse()
    reversed_song.export(f"testdata/reversed_{filename}.mp3", format="mp3")

    def generate():
        with open(f"testdata/reversed_{filename}.mp3", "rb") as fmp3:
            data = fmp3.read(1024)
            while data:
                yield data
                data = fmp3.read(1024)

    return Response(generate(), mimetype="audio/mp3")


if __name__ == "__main__":
    app.run(debug=True)
