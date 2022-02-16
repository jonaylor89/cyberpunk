import yaml


class CyberpunkConfig:
    def __init__(
        self,
        port: int = 5000,
        audio_store: str = "local",
        storage_base_dir: str = "testdata/",
        s3_storage_bucket: str = "mybucket",
        s3_storage_base_dir: str = "audio/",
    ):
        self.port = port

        # local | s3 | audius
        self.audio_store = audio_store

        self.local_storage = LocalStorageConfig(storage_base_dir)
        self.s3_storage = S3StorageConfig(
            s3_storage_bucket,
            s3_storage_base_dir,
        )

    @classmethod
    def from_yaml(cls, path="cyberpunk.yaml"):
        with open(path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        # TODO: validation lol
        port = data["port"]
        audio_source = data["audio_store"]
        storage_base_dir = data["local"]["storage_base_dir"]
        s3_storage_bucket = data["s3"]["s3_storage_bucket"]
        s3_storage_base_dir = data["s3"]["s3_storage_base_dir"]

        return cls(
            port,
            audio_source,
            storage_base_dir,
            s3_storage_bucket,
            s3_storage_base_dir,
        )


class LocalStorageConfig:
    def __init__(self, storage_base_dir: str = "testdata/"):
        self.storage_base_dir = storage_base_dir


class S3StorageConfig:
    def __init__(
        self,
        s3_storage_bucket: str = "mybucket",
        s3_storage_base_dir: str = "audio/",
    ):
        self.s3_storage_bucket = s3_storage_bucket
        self.s3_storage_base_dir = s3_storage_base_dir


# Cyberpunk Config Singleton
cyberpunk_config = CyberpunkConfig.from_yaml("cyberpunk.yaml")
