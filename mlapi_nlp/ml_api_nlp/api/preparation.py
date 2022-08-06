from pathlib import Path

basedir = Path(__file__).parent.parent


def get_req_text(request):
    """画像の読み込み"""
    text = request.json["text"]
    print(f"request_text: {text}")
    return text