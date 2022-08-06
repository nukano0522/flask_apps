from ml_api_nlp.api.config.base import Config


class LocalConfig(Config):
    TESTING = True
    DEBUG = True