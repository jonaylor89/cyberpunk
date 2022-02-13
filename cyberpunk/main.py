from typing import Generator
from pydub import AudioSegment

from flask import Flask, Response

app = Flask(__name__)


def stream_audio_file(filename: str, chunk_size: int = 1024) -> Generator:
    with open(f"testdata/{filename}", "rb") as faudio:
        data = faudio.read(chunk_size)
        while data:
            yield data
            data = faudio.read(chunk_size)


@app.route("/")
def hello():
    return "Hello World"


@app.route("/audio/<filename>")
def stream_mp3(filename: str):
    return Response(stream_audio_file(f"{filename}"), mimetype="audio/mp3")


@app.route("/reverse/<filename>")
def stream_reverse(filename: str):
    song = AudioSegment.from_mp3(f"testdata/{filename}")
    reversed_song = song.reverse()
    reversed_song.export(f"testdata/reversed_{filename}", format="mp3")

    return Response(stream_audio_file(f"reversed_{filename}"), mimetype="audio/mp3")


@app.route("/repeat/<int:multiplier>/<filename>")
def stream_repeat(filename: str, multiplier: int):
    song = AudioSegment.from_mp3(f"testdata/{filename}")
    repeated_song = song * multiplier
    repeated_song.export(f"testdata/repeat_{multiplier}_{filename}", format="mp3")

    return Response(
        stream_audio_file(f"repeat_{multiplier}_{filename}"), mimetype="audio/mp3"
    )


@app.route("/slice/<int:start>/<int:end>/<filename>")
def stream_repeat(filename: str, start: int, end: int):
    song = AudioSegment.from_mp3(f"testdata/{filename}")
    sliced_song = song[start:end]
    sliced_song.export(f"testdata/slice_{start}_{end}_{filename}", format="mp3")

    return Response(
        stream_audio_file(f"slice_{start}_{end}_{filename}"), mimetype="audio/mp3"
    )


if __name__ == "__main__":
    app.run(debug=True)
