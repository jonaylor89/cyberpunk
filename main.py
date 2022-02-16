#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from cyberpunk.server import create_app

# TODO: Use `click` cli package to create cyberpunk cli
# e.g. cyberpunk serve, cyberpunk serve --config=/some/path/config.yaml,


app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        load_dotenv=True,
        port=int(os.environ.get("PORT", 5000)),
    )
