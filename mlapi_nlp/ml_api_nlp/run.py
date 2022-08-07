import os

from flask import Flask

from ml_api_nlp.api import api
from ml_api_nlp.api.config import config_case

config_name = os.environ.get("CONFIG", "dev")

app = Flask(__name__)
app.config.from_object(config_case[config_name])
# blueprintをアプリケーションに登録
app.register_blueprint(api)