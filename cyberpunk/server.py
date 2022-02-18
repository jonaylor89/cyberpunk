import logging
import logging.config
from typing import Generator

from flask import Flask, Response, jsonify, request, stream_with_context

from cyberpunk.config import configure_config
from cyberpunk.logger_config import LoggerConfig
from cyberpunk.processing import parse_query, process_args
from cyberpunk.storage import configure_storage


def create_app(config: str = "cyberpunk.yaml"):
    configure_config(config)
    configure_storage()

    app = Flask(__name__)

    # 'always' (default), 'never',  'production', 'debug'
    app.config["LOGGER_HANDLER_POLICY"] = "always"

    # define which logger to use for Flask
    app.config["LOGGER_NAME"] = "cyberpunk"

    #  initialise logger
    app.logger

    logging.config.dictConfig(LoggerConfig.dictConfig)

    def stream_audio_file(filename: str, chunk_size: int = 2048) -> Generator:
        with open(f"testdata/{filename}", "rb") as faudio:
            data = faudio.read(chunk_size)
            while data:
                yield data
                data = faudio.read(chunk_size)

    @app.route("/")
    def hello():
        return "Hello World"

    @app.route("/health")
    def healthcheck():
        return 200

    @app.route("/params/<filename>", methods=["GET"])
    def params_route(filename: str):
        """
        Route to format URL parameters as
        json to validate them before sending
        them to the `unsafe_processing` route
        """
        return jsonify(parse_query(filename, request.args))

    @app.route("/unsafe/<filename>", methods=["GET"])
    def unsafe_processing(filename: str):
        """
        Route to run processing pipeline on an audio file

        It's considered unsafe because there's currently no authentication or validation
        """
        args = request.args
        processed_file, file_type = process_args(filename, args)

        return Response(
            stream_with_context(stream_audio_file(processed_file)),
            mimetype=file_type,
        )

    @app.route("/tag/<filename>", methods=["GET"])
    def tag_audio_route(filename: str):
        """
        Route to get tags from audio files
        """
        return {
            "file_key": filename,
            "tags": [
                "cool",
                "awesome",
                "country",
                "hiphop",
                "fast",
                "chill",
            ],
        }

    @app.route("/stats", methods=["GET"])
    def storage_stats_route():
        """
        Route to get state on the audio store backend

        What's returned will depend on the audio store configured (local, s3, audius)
        """
        return {
            "tracks": 13019,
            "total time": "4.9 weeks",
            "total size": "71.1 GB",
            "artists": 548,
            "albums": 1094,
        }

    return app
