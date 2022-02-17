
# Cyberpunk

Audio Processing Server

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/jonaylor89/cyberpunk/Docker)

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/jonaylor89/cyberpunk)

# Install

With Poetry
```sh
curl -sSL https://install.python-poetry.org | python3 -
poetry run main.py
```

With Docker
```
docker pull ghcr.io/jonaylor89/cyberpunk:sha256-36a2ec3c572d69b41a096cee07f60f2e07d669846ceb0dd8b9f54d741ecc678c.sig
docker run -e PORT=8080 jonaylor/cyberpunk
```


# Features

- [x] Audio Streaming

- [ ] Change encodings (e.g. mp3 -> wav)
- [x] Audio slicing
- [ ] Change Volume
- [ ] Concat Audio
- [x] Repeat Audio
- [x] Reverse Audio
- [ ] Crossfade
- [ ] Fade in/out
- [ ] Audio Quality
- [ ] Audio Tagging
- [ ] Audio Thumbnails
- [ ] Mastering Music

- [ ] Sound/Vocal Isolation

- [ ] [Cool ML Stuff](https://github.com/spotify/pedalboard)

- [ ] [File Caching](https://gist.github.com/ruanbekker/75d98a0d5cab5d6a562c70b4be5ba86d)

# Storage Options

- [x] Local
- [ ] Cloud (e.g. S3)
- [x] Blockchain (Audius)


# Environment

CYBERPUNK_SECRET: mysecret # secret key for URL signature

AWS_ACCESS_KEY_ID: ...

AWS_SECRET_ACCESS_KEY: ...

AWS_REGION: us-east-1