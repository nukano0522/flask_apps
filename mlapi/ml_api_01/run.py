import os

from flask import Flask

from ml_api_01.api import api, tmp
from ml_api_01.api import tmp
from ml_api_01.api.config import config

# print(f"run.pyのtmp: {tmp}")
config_name = os.environ.get("CONFIG", "local")

app = Flask(__name__)
app.config.from_object(config[config_name])
# blueprintをアプリケーションに登録
app.register_blueprint(api)