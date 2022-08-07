from flask import Blueprint, jsonify, request

from ml_api_nlp.api import prediction

api = Blueprint("api", __name__)

@api.get("/")
def index():
    return jsonify({"test": "hogehoge"}), 201


@api.post("/predict")
def predict():
    return prediction.bert_prediction(request)