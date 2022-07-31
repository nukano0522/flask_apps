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
