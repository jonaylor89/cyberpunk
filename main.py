#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import click

from cyberpunk import __version__
from cyberpunk.server import create_app

app = create_app()


@click.command()
@click.version_option(__version__)
@click.option("--debug", is_flag=True)
@click.option(
    "--config",
    type=click.Path(exists=True),
    default="cyberpunk.yaml",
    help="Cyberpunk config file",
)
@click.option(
    "--port",
    type=click.INT,
    default=lambda: os.environ.get("PORT", 5000),
    help="Server port number",
)
def main(debug, config, port):
    server = create_app(config)
    server.run(
        debug=debug,
        load_dotenv=True,
        port=int(port),
    )


if __name__ == "__main__":
    main()
