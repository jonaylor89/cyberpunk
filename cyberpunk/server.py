import logging
import logging.config
from typing import Generator, Optional

from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    request,
    stream_with_context,
)

from cyberpunk.config import CyberpunkConfig, configure_config
from cyberpunk.logger_config import LoggerConfig
from cyberpunk.processing import parse_query, process_args
from cyberpunk.storage import configure_storage

# from musicnn.tagger import top_tags


def create_app(cyberpunk_config: Optional[CyberpunkConfig] = None):
    configure_config(provided_config=cyberpunk_config)
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
        with open(f"/tmp/{filename}", "rb") as faudio:
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

    @app.route("/params/<path:filename>", methods=["GET"])
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
        logging.critical(f"file path: {filename}, args: {args}")
        processed_file, file_type = process_args(filename, args)

        return Response(
            stream_with_context(stream_audio_file(processed_file)),
            mimetype=file_type,
        )

    @app.route("/unsafe/https://<path:url>", methods=["GET"])
    def unsafe_https_processing(url: str):
        """
        Route to run processing pipeline on an audio file

        It's considered unsafe because there's currently no authentication or validation
        """
        args = request.args
        logging.critical(f"file path: {url}, args: {args}")
        processed_file, file_type = process_args(f"https://{url}", args)

        return Response(
            stream_with_context(stream_audio_file(processed_file)),
            mimetype=file_type,
        )

    @app.route("/unsafe/http://<path:url>", methods=["GET"])
    def unsafe_http_processing(url: str):
        """
        Route to run processing pipeline on an audio file

        It's considered unsafe because there's currently no authentication or validation
        """
        args = request.args
        logging.critical(f"file path: {url}, args: {args}")
        processed_file, file_type = process_args(f"http://{url}", args)

        return Response(
            stream_with_context(stream_audio_file(processed_file)),
            mimetype=file_type,
        )

    @app.route("/tag/<filename>", methods=["GET"])
    def tag_audio_route(filename: str):
        """
        Route to get tags from audio files
        """

        # features = top_tags(f'./testdata/{filename}.mp3', model='MTT_musicnn', topN=10)
        features = [
            "hiphop",
            "drums",
            "fast",
        ]

        return {
            "file_key": filename,
            "tags": features,
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

    @app.errorhandler(404)
    def not_found(error):
        """Page not found."""
        print(error)
        print(request.url)
        print(request.args)
        return make_response("Route not found", 404)

    return app
