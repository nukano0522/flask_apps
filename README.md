# flask_apps


# AzureWebAppsへのデプロイ

# デプロイ後はdb構成のマイグレーション（DB情報の差分を反映する）
- azurewebappサーバーにSSH接続
- flask db init
- flask db migrate
- flask db upgrade(downgrade)

# 実行するアプリファイルがapp.py（application.py）以外のとき
gunicornによるスタートアップ構成が必要
AzurePortal→webapp→構成→全般設定→スタートアップコマンド
https://docs.microsoft.com/ja-jp/azure/developer/python/configure-python-web-app-on-app-service#flask-startup-commands

デプロイするフォルダのルートにstartup.shを配置し、実行するアプリを記述
例：
gunicorn --bind=0.0.0.0 --timeout 600 autoapp:app
gunicorn --bind=0.0.0.0 --timeout 600 --chdir ml_api_01 run:app

# ターミナルからAPIにPOSTする
curl -X POST https://flask-ml-api-02.azurewebsites.net/detect -H "Content-Type:application/json" -d '{"filename": "DSC_0173.JPG"}'
curl -X POST http://127.0.0.1:5000/detect -H "Content-Type:application/json" -d '{"filename": "DSC_0173.JPG"}'
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type:application/json" -d '{"text": "27日に生放送された日本テレビ「バンクーバー2010」には、女子フィギュアスケートで銀メダルを獲得した浅田真央が出演した。\n\nメダルを獲得しながらも、自身の演技に満足できず悔し涙を流した運命の日から一夜明け、プレッシャーから解放された安堵感からか、いつもの笑顔がみられるようになった浅田。五輪史上初となる3度のトリプルアクセル（3回転半）を成功させたことには、「今シーズンから3回飛ぶって決めてましたし、それをやりたいっていう思いがあったのでオリンピックで挑戦というよりは、やってきたことを出したいという思いが強かったです」と語った。\n\nまた、五輪という舞台については、「予想していたよりも、すごい大きな舞台だったんだなって、終わってから改めて感じました」と振り返る浅田は、同番組が生放送されることで出演前から緊張していた点に話が及ぶと、「生なんだと。流れてるんだと、日本で・・・」と苦笑いを浮かべた。"}'

curl -X POST http://127.0.0.1:5000/predict -H "Content-Type:application/json" -d '{"text": "I like a cat"}'

curl -X POST http://127.0.0.1:5000/predict -H 'Content-Type:application/json' -d @post_text.json

# 課題
- opencvのビルド
- モデルの読み込み
    - +cpuのtorch(torchvision)には必要なクラスが定義されていない
    　→自分でモデルクラスを作ってみる
    - modelクラスを定義してstate_dictする必要ある？
    - →テキストの推論でやってみる


vim antenv/lib/python3.9/site-packages/torchvision/ops/misc.py