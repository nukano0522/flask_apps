from pathlib import Path

import torch
from transformers import BertJapaneseTokenizer
from flask import current_app, jsonify

from ml_api_nlp.api.preparation import get_req_text
from ml_api_nlp.api.preprocess import text_to_loader
from ml_api_nlp.api.bert_model import BertForLivedoor

basedir = Path(__file__).parent.parent

def bert_prediction(request):
    # print(f"request: {vars(request)}")
    tokenizer = BertJapaneseTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-whole-word-masking")
    # ラベルの読み込み
    # labels = current_app.config["LABELS"]
    
    # テキストの読み込み
    text = get_req_text(request)
    # データローダに変換
    dataloader = text_to_loader(text, tokenizer)

    # BERTモデル
    net_trained = BertForLivedoor()

    # 学習済みモデルの読み込み
    try:
        # モデル読み込み
        save_path = "./single_bert_fine_tuning_livedoor.pth"
        net_trained.load_state_dict(torch.load(save_path, map_location=torch.device('cpu')))
    except FileNotFoundError:
        return jsonify("The model is not found"), 404

    # モデルの推論モードに切り替え
    net_trained.eval()

    # GPUが使えるならGPUにデータを送る
    batch = next(iter(dataloader))
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    inputs = batch["ids"][0].to(device)  # 文章

    # 推論の実行
    outputs = net_trained(inputs)
    _, pred = torch.max(outputs, 1)  # ラベルを予測

    pred_num = pred.to('cpu').detach().numpy()[0]

    print(f"pred: {pred_num}")

    return jsonify({"pred": str(pred_num)}), 201