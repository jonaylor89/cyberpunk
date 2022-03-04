
# Cyberpunk

Audio Processing Server

![GitHub](https://img.shields.io/github/license/jonaylor89/cyberpunk?logo=MIT) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/jonaylor89/cyberpunk/Docker)

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run?git_repo=https://github.com/jonaylor89/cyberpunk)


### Quick Start

```sh
docker run -p 8080:8080 -e PORT=8080 ghcr.io/jonaylor89/cyberpunk:main
```

Original audio:
```sh
https://raw.githubusercontent.com/jonaylor89/cyberpunk/main/testdata/celtic_pt2.mp3
```

![](testdata/celtic_pt2.mp3)


Try out the following audio URLs:
```
http://localhost:8000/unsafe/https://raw.githubusercontent.com/jonaylor89/cyberpunk/main/testdata/celtic_pt2.mp3
http://localhost:8000/unsafe/https://raw.githubusercontent.com/jonaylor89/cyberpunk/main/testdata/celtic_pt2.mp3?reverse=true
http://localhost:8000/unsafe/https://raw.githubusercontent.com/jonaylor89/cyberpunk/main/testdata/celtic_pt2.mp3?slice=0:10000
http://localhost:8000/unsafe/https://raw.githubusercontent.com/jonaylor89/cyberpunk/main/testdata/celtic_pt2.mp3?reverse=true&repeat=1&slice=1000:5000

```

### Cyberpunk Endpoint

Cyberpunk endpoint is a series of URL parts which defines the image operations, followed by the image URI:

```
/HASH|unsafe/AUDIO?slice&concat&fade_in&fade_out&repeat&reverse&filters=NAME(ARGS)
```

- `HASH` is the URL Signature hash, or `unsafe` if unsafe mode is used
- `slice`
- `concat`
- `fade_in`
- `fade_out`
- `repeat`
- `reverse`
- `AUDIO` is the audio URI


Cyberpunk provides utilities for previewing and generating Cyberpunk endpoint URI, including the [cyberpunk_path](https://github.com/jonaylor89/cyberpunk/tree/main/cyberpunk/processing.py) function and the `/params` endpoint:

#### `GET /params`

Prepending `/params` to the existing endpoint returns the endpoint attributes in JSON form, useful for preview:

```sh
curl "http://localhost:8000/unsafe/celtic_p2.mp3?reverse=true&repeat=1&slice=1000:5000"

{
  "audio": "celtic_pt2.mp3",
  "hash": "unsafe",
  "reverse": true,
  "repeat": 1,
  "slice": {
      "start": 1000,
      "end": 5000,
  }
}
```

### Features

- [x] Audio Streaming

- [x] Change encodings (e.g. mp3 -> wav)
- [x] Audio slicing
- [ ] Change Volume
- [x] Concat Audio
- [x] Repeat Audio
- [x] Reverse Audio
- [ ] Crossfade
- [x] Fade in/out
- [ ] Audio Quality
- [ ] Audio Tagging
- [ ] Audio Thumbnails
- [ ] Mastering Music

- [ ] Sound/Vocal Isolation

- [ ] [Cool ML Stuff](https://github.com/spotify/pedalboard)

- [ ] [File Caching](https://gist.github.com/ruanbekker/75d98a0d5cab5d6a562c70b4be5ba86d)

### Storage Options

- [x] Local
- [ ] Cloud (e.g. S3)
- [x] Blockchain (Audius)


### Environment

PORT: 8080 # server port number

CYBERPUNK_SECRET: mysecret # secret key for URL signature

AWS_ACCESS_KEY_ID: ...

AWS_SECRET_ACCESS_KEY: ...

AWS_REGION: us-east-1

AUDIO_PATH=local:s3:audius:http

STORAGE_BASE_DIR=testdata/

RESULTS_STORAGE_BASE_DIR=processed/

S3_LOADER_BUCKET=mybucket

S3_LOADER_BASE_DIR=audio/

S3_STORAGE_BUCKET=mybucket

S3_STORAGE_BASE_DIR=audio/

S3_RESULTS_STORAGE_BUCKET=mybucket

S3_RESULTS_STORAGE_BASE_DIR=audio/results


# Docker Compose Example

Cyberpunk with file system, using mounted volume:

```yaml
version: "3"
services:
  imagor:
    image: jonaylor/cyberpunk:main
    volumes:
      - ./:/mnt/data
    environment:
      PORT: 8080
      AUDIO_PATH: "local"
      FILE_STORAGE_BASE_DIR: /mnt/data/testdata/ # enable file storage by specifying base dir
    ports:
      - "8080:8080"
```

Cyberpunk with AWS S3:

```yaml
version: "3"
services:
  imagor:
    image: jonaylor/cyberpunk:main
    environment:
      PORT: 8080
      CYBERPUNK_SECRET: mysecret # secret key for URL signature
      AWS_ACCESS_KEY_ID: ...
      AWS_SECRET_ACCESS_KEY: ...
      AWS_REGION: ...

      AUDIO_PATH: "s3"

      S3_LOADER_BUCKET: mybucket # enable S3 loader by specifying bucket
      S3_LOADER_BASE_DIR: audio # optional

      S3_STORAGE_BUCKET: mybucket # enable S3 storage by specifying bucket
      S3_STORAGE_BASE_DIR: audio # optional

      S3_RESULT_STORAGE_BUCKET: mybucket # enable S3 result storage by specifying bucket
      S3_RESULT_STORAGE_BASE_DIR: audio/result # optional
    ports:
      - "8080:8080"
```