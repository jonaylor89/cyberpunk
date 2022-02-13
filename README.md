
# Cyberpunk 

Audio Processing Server

# Features

- [_] Change encodings (e.g. mp3 -> wav) 
- [_] Audio slicing 
- [_] Change Volume 
- [_] Concat Audio 
- [x] Repeat Audio 
- [x] Reverse Audio 
- [_] Crossfade 
- [_] Fade in/out   
- [_] Audio Quality 
- [_] Audio Tagging 
- [_] Audio Thumbnails 
- [_] Mastering Music 

# Storage Options

- Local
- Cloud (e.g. S3)
- Blockchain (Audius)


# Environment

PORT: 8000

SOUNDBISS_SECRET: mysecret # secret key for URL signature

AWS_ACCESS_KEY_ID: ...

AWS_SECRET_ACCESS_KEY: ...

AWS_REGION: us-east-1

S3_LOADER_BUCKET: mybucket # enable S3 loader by specifying bucket

S3_LOADER_BASE_DIR: audio # optional

S3_STORAGE_BUCKET: mybucket # enable S3 storage by specifying bucket

S3_STORAGE_BASE_DIR: audio # optional

S3_RESULT_STORAGE_BUCKET: mybucket # enable S3 result storage by specifying bucket

S3_RESULT_STORAGE_BASE_DIR: audio/result # optional


