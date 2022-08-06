from ml_api_01.api.config.base import Config


class LocalConfig(Config):
    TESTING = True
    DEBUG = True