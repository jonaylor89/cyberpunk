from typing import Generator
from flask import Flask, Response, stream_with_context, jsonify, request

##############################

from cyberpunk.processing import parse_query, process_args
from cyberpunk.config import cyberpunk_config

##############################


def create_app():
    app = Flask(__name__)

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
    def unsafe_processing(filename: str):
        args = request.args
        processed_file, file_type = process_args(filename, args)

        return Response(
            stream_with_context(stream_audio_file(processed_file)), mimetype=file_type
        )

    @app.route("/params/<filename>")
    def params_route(filename: str):
        return jsonify(parse_query(filename, request.args))

    return app
