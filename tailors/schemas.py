from oss2 import Auth, Bucket
from pydantic import BaseModel, BaseSettings, HttpUrl


class OSSClient(BaseModel):
    access_key: str
    access_secret: str
    endpoint: HttpUrl
    bucket_name: str

    def get_bucket(self):
        auth = Auth(self.access_key, self.access_secret)
        bucket = Bucket(auth, self.endpoint, self.bucket_name)
        return bucket


class AppSettings(BaseSettings):
    oss: OSSClient

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
