from pydantic import BaseSettings


class LoggingSettings(BaseSettings):
    level: str = 'INFO'
    format: str = '%(asctime)s %(levelname)s: %(message)s'


class IpfsSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 5001


class AppSettings(BaseSettings):

    ipfs: IpfsSettings = IpfsSettings()
    logging_settings: LoggingSettings = LoggingSettings()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
