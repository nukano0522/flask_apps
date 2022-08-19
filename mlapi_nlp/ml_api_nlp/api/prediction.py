
import torch
from transformers import BertJapaneseTokenizer
from flask import current_app, jsonify

from ml_api_nlp.api.preprocess import get_req_text, text_to_loader
from ml_api_nlp.api.bert_model import BertModel


def bert_prediction(request):
    
    tokenizer = BertJapaneseTokenizer.from_pretrained("cl-tohoku/bert-base-japanese-whole-word-masking")
    
    # テキストの読み込み
    texts = get_req_text(request)
    
    # データローダに変換
    dataloader = text_to_loader(texts, tokenizer)

    # BERTモデル
    net_trained = BertModel()

    # 学習済みモデルの読み込み
    try:
        # モデル読み込み
        print("Loading model ...")
        save_path = "./single_bert_fine_tuning_livedoor.pth"
        net_trained.load_state_dict(torch.load(save_path, map_location=torch.device('cpu')))
        print("... Complete.")
    except FileNotFoundError:
        return jsonify("The model is not found"), 404

    # モデルの推論モードに切り替え
    net_trained.eval()

    # # GPUが使えるならGPUにデータを送る
    batch = next(iter(dataloader))
    print(f"Batch Size: {batch['ids'][0].size()}")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    inputs = batch["ids"][0].to(device)  # 文章

    # 推論の実行
    print("Infer is processing ...")
    outputs = net_trained(inputs)
    print("... Complete.")
    
    _, preds = torch.max(outputs, 1)  # ラベルを予測
    print(f"preds: {preds}")

    preds_num = preds.to('cpu').detach().numpy()
    print(f"preds_num: {preds_num}")

    # レスポンスデータ
    results = []
    for i, p in enumerate(preds_num):
        res = {}
        res["text"] = batch["text"][i][0:20] + "..."
        res["pred"] = current_app.config["ID2LABEL"][p]
        res["pred_label"] = str(p)
        results.append(res)

    current_app.config["JSON_AS_ASCII"] = False
    return jsonify({"results": results})
