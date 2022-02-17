#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import click

from cyberpunk.server import create_app

# TODO: Use `click` cli package to create cyberpunk cli
# e.g. cyberpunk serve, cyberpunk serve --config=/some/path/config.yaml,


app = create_app()


@click.command()
@click.option(
    "--config",
    default="cyberpunk.yaml",
    help="Cyberpunk config file",
)
def main(config):
    server = create_app()
    print(config)
    server.run(
        debug=True,
        load_dotenv=True,
        port=int(os.environ.get("PORT", 5000)),
    )


if __name__ == "__main__":
    main()
