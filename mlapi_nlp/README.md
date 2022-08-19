# Flask+AzureWebAppsによる機械学習API

## 環境

## 前提

## ローカルでFlaskAPIを実行
- 実行アプリがあるディレクトリ（run.py）で`flask run`

## Azureにデプロイ、APIを実行

### 実行するアプリファイルがapp.py（application.py）以外のとき
gunicornによるスタートアップ構成が必要
AzurePortal→webapp→構成→全般設定→スタートアップコマンド
https://docs.microsoft.com/ja-jp/azure/developer/python/configure-python-web-app-on-app-service#flask-startup-commands

デプロイするフォルダのルートにstartup.shを配置し、実行するアプリを記述
例：
gunicorn --bind=0.0.0.0 --timeout 600 autoapp:app
gunicorn --bind=0.0.0.0 --timeout 600 --chdir ml_api_nlp run:app

### VSCodeからDBHOSTやDBNAMEなどの情報を設定する
- デプロイ環境の環境変数に設定される
https://docs.microsoft.com/ja-jp/azure/app-service/tutorial-python-postgresql-app?tabs=flask%2Cwindows%2Cazure-portal%2Cterminal-bash%2Cazure-portal-access%2Cvscode-aztools-deploy%2Cdeploy-instructions-azportal%2Cdeploy-instructions--zip-azcli%2Cdeploy-instructions-curl-bash

### デプロイ
- デプロイするフォルダに移動して、Azureにデプロイする
- 「VSCodeのAzure→RESOURCES→サブスクリプション→AppServices→対象のアプリ」で右クリックして、Deploy to Web App...
- デプロイのログは、AzurePortalのAppServiceのデプロイセンターから確認可能

## ターミナルからAPIにPOSTする
例：
```
curl -X POST http://127.0.0.1:5000/predict -H 'Content-Type:application/json' -d @request_data/request-ok.json
curl -X POST https://flask-ml-api-06.azurewebsites.net/predict -H 'Content-Type:application/json' -d @request_data/request-ok.json
```

## デプロイ後はdb構成のマイグレーション ※DB利用する場合
- azurewebappサーバーにSSH接続
- flask db init
- flask db migrate
- flask db upgrade(downgrade)