#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cyberpunk.main import create_app
from cyberpunk.config import cyberpunk_config

if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=True,
        load_dotenv=True,
        port=cyberpunk_config.port,
    )
