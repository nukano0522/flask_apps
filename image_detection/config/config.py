from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(f"BASE_DIR: {BASE_DIR}")

class CommonConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"
    # 画像アップロード先にapps/imagesを指定する
    UPLOAD_FOLDER = str(Path(BASE_DIR, "images"))

    # 物体検知に利用するラベル
    LABELS = [
        "unlabeled",
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "street sign",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "hat",
        "backpack",
        "umbrella",
        "shoe",
        "eye glasses",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "plate",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "mirror",
        "dining table",
        "window",
        "desk",
        "toilet",
        "door",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "blender",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]

class DevConfig(CommonConfig):

    SECRET_KEY = "hogehoge"

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ['DBUSER'],
        dbpass=os.environ['DBPASS'],
        dbhost=os.environ['DBHOST'],
        dbname=os.environ['DBNAME']
    )

    TIME_ZONE = 'UTC'

    STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
    STATIC_URL = 'static/'


class ProdConfig(CommonConfig):
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'flask-insecure-7ppocbnx@w71dcuinn*t^_mzal(t@o01v3fee27g%rg18fc5d@'

    DEBUG = False
    ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
    CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

    # Configure Postgres database; the full username for PostgreSQL flexible server is
    # username (not @sever-name).
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ['DBUSER'],
        dbpass=os.environ['DBPASS'],
        dbhost=os.environ['DBHOST'] + ".postgres.database.azure.com",
        dbname=os.environ['DBNAME']
    )