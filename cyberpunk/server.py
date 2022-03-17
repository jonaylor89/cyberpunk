import logging
import logging.config
import uuid
from typing import Generator, Optional

from flask import (
    Flask,
    Response,
    after_this_request,
    jsonify,
    make_response,
    request,
    stream_with_context,
)
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from cyberpunk.config import CyberpunkConfig, configure_config
from cyberpunk.logger_config import LoggerConfig
from cyberpunk.processing import parse_query, process_args
from cyberpunk.storage import configure_storage

# from musicnn.tagger import top_tags


def create_app(cyberpunk_config: Optional[CyberpunkConfig] = None):
    configure_config(provided_config=cyberpunk_config)
    configure_storage()

    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({SERVICE_NAME: "cyberpunk"})),
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter()),
    )

    # TODO : make agent_host_name & agent_port configurable
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
    )

    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(jaeger_exporter),
    )

    app = Flask(__name__)
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("foo"):
        with tracer.start_as_current_span("bar"):
            with tracer.start_as_current_span("baz"):
                print("Hello world from OpenTelemetry Python!")

    # 'always' (default), 'never',  'production', 'debug'
    app.config["LOGGER_HANDLER_POLICY"] = "always"

    # define which logger to use for Flask
    app.config["LOGGER_NAME"] = "cyberpunk"

    #  initialise logger
    app.logger

    logging.config.dictConfig(LoggerConfig.dictConfig)

    def stream_audio_file(filename: str, chunk_size: int = 4096) -> Generator:
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

    @app.route("/params/<path:key>", methods=["GET"])
    def params_route(key: str):
        """
        Route to format URL parameters as
        json to validate them before sending
        them to the `unsafe_processing` route
        """
        # TODO : Add tracer
        return jsonify(parse_query(key, request.args))

    @app.route("/unsafe/<key>", methods=["GET"])
    def unsafe_processing(key: str):
        """
        Route to run processing pipeline on an audio file

        It's considered unsafe because there's currently no authentication or validation
        """
        # TODO : Add tracer
        request_id = uuid.uuid4()
        args = request.args
        processed_file, file_type = process_args(request_id, key, args)

        @after_this_request
        def delete_tmp_file(response):
            return response

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

        # TODO : Add tracer
        request_id = uuid.uuid4()
        args = request.args
        logging.critical(f"file path: {url}, args: {args}")
        processed_file, file_type = process_args(
            request_id,
            f"https://{url}",
            args,
        )

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

        # TODO : Add tracer
        request_id = uuid.uuid4()
        args = request.args
        logging.critical(f"file path: {url}, args: {args}")
        processed_file, file_type = process_args(
            request_id,
            "http://{url}",
            args,
        )

        return Response(
            stream_with_context(stream_audio_file(processed_file)),
            mimetype=file_type,
        )

    @app.route("/tag/<filename>", methods=["GET"])
    def tag_audio_route(filename: str):
        """
        Route to get tags from audio files
        """
        # TODO: add tagging
        # TODO : Add tracer
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

        # TODO : implement stats route
        # TODO : Add tracer
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
        # TODO : Add tracer
        return make_response("Route not found", 404)

    return app
