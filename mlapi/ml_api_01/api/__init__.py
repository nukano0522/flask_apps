from flask import Blueprint, jsonify, request

from ml_api_01.api import calculation

api = Blueprint("api", __name__)
tmp = "hogehoge"
print(f"__init__.pyのtmp: {tmp}")

@api.get("/")
def index():
    return jsonify({"column": "value"}), 201


@api.post("/detect")
def detection():
    return calculation.detection(request)