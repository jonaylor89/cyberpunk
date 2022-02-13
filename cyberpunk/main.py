
from typing import Generator
from pydub import AudioSegment
from flask import Flask, Response, stream_with_context, jsonify, request

##############################

from .parse import parse_url

##############################

app = Flask(__name__)


@stream_with_context
def stream_audio_file(filename: str, chunk_size: int = 2048) -> Generator:
    with open(f"testdata/{filename}", "rb") as faudio:
        data = faudio.read(chunk_size)
        while data:
            yield data
            data = faudio.read(chunk_size)


@app.route("/")
def hello():
    return "Hello World"


@app.route("/healthcheck")
def healthcheck():
    return 200


@app.route("/unsafe/<filename>", methods=["GET"])
def stream_mp3(filename: str):
    args = request.args
    print(args)

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
def stream_slice(filename: str, start: int, end: int):
    song = AudioSegment.from_mp3(f"testdata/{filename}")
    sliced_song = song[start:end]
    sliced_song.export(f"testdata/slice_{start}_{end}_{filename}", format="mp3")

    return Response(
        stream_audio_file(f"slice_{start}_{end}_{filename}"), mimetype="audio/mp3"
    )


@app.route("/params/<filename>")
def params_route(filename: str):
    return jsonify(parse_query(filename, request.args))


if __name__ == "__main__":
    app.run(debug=True, load_dotenv=True)
