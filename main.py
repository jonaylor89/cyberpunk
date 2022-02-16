#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cyberpunk.server import create_app
from cyberpunk.config import cyberpunk_config

# TODO: Use `click` cli package to create cyberpunk cli
# e.g. cyberpunk serve, cyberpunk serve --config=/some/path/config.yaml, 


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        load_dotenv=True,
        port=cyberpunk_config.port,
    )
