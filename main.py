#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import click

from cyberpunk.server import create_app

app = create_app()


@click.command()
@click.option(
    "--config",
    default="cyberpunk.yaml",
    help="Cyberpunk config file",
)
@click.option(
    "--port",
    type=click.INT,
    default=lambda: os.environ.get("PORT", 5000),
    help="Server port number",
)
def main(config, port):
    server = create_app()
    print(config)
    server.run(
        debug=True,
        load_dotenv=True,
        port=int(port),
    )


if __name__ == "__main__":
    main()
