from ml_api_01.api.config import base, local
# import inspect
# print(f"{__name__}の呼び出し元ファイル:{inspect.stack()[0][1]}")

config = {
    "base": base.Config,
    "local": local.LocalConfig,
}