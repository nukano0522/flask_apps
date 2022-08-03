import numpy as np
import uuid
from pathlib import Path
import random
import torch, torchvision
import cv2
from PIL import Image
from sqlalchemy.exc import SQLAlchemyError
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from .forms import UploadImageForm, DeleteForm, DetectorForm

from .models import UserImage, UserImageTag
import os, sys
sys.path.append('../')
from app import db
from crud.models import User

# template_folderを指定する（staticは指定しない）
dt = Blueprint("detector", __name__, template_folder="templates")

# dtアプリケーションを使ってエンドポイントを作成する
@dt.route("/")
def index():
    # UserとUserImageをJoinして画像一覧を取得する
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )

    # タグ一覧を取得する
    user_image_tag_dict = {}
    for user_image in user_images:
        # 画像に紐づくタグ一覧を取得する
        user_image_tags = (
            db.session.query(UserImageTag)
            .filter(UserImageTag.user_image_id == user_image.UserImage.id)
            .all()
        )
        user_image_tag_dict[user_image.UserImage.id] = user_image_tags

    # 物体検知フォームをインスタンス化する
    detector_form = DetectorForm()
    # DeleteFormをインスタンス化する
    delete_form = DeleteForm()

    return render_template(
        "detector/index.html",
        user_images=user_images,
        # タグ一覧をテンプレートに渡す
        user_image_tag_dict=user_image_tag_dict,
        # 物体検知フォームをテンプレートに渡す
        detector_form=detector_form,
        # 画像削除フォームをテンプレートに渡す
        delete_form=delete_form,
    )


@dt.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@dt.route("/upload", methods=["GET", "POST"])
def upload_image():
    # UploadImageFormを利用してバリデーションをする
    form = UploadImageForm()
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得する
        file = form.image.data

        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        # 画像を保存する
        image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
        file.save(image_path)

        # DBに保存する
        # user_image = UserImage(user_id=current_user.id, image_path=image_uuid_file_name) # ログイン機能ある場合
        user_image = UserImage(user_id=1, image_path=image_uuid_file_name) # ログイン機能ない場合はuser_id=1で固定
        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for("detector.index"))
    return render_template("detector/upload.html", form=form)


@dt.route("/images/delete/<string:image_id>", methods=["POST"])
def delete_image(image_id):
    try:
        # imageフォルダのファイルも削除する
        delete_image = db.session.query(UserImage).filter(UserImage.id == image_id).first()
        delete_image_path = Path(current_app.config["UPLOAD_FOLDER"], delete_image.image_path)
        delete_image_withTag_path = Path(current_app.config["UPLOAD_FOLDER"], delete_image.image_withTag_path)
        os.remove(delete_image_path)
        os.remove(delete_image_withTag_path)

        # user_image_tagsテーブルからレコードを削除する
        db.session.query(UserImageTag).filter(
            UserImageTag.user_image_id == image_id
        ).delete()

        # user_imageテーブルからレコードを削除する
        db.session.query(UserImage).filter(UserImage.id == image_id).delete()
        db.session.commit()

    except Exception as e:
        flash("画像削除処理でエラーが発生しました。")
        # エラーログ出力
        current_app.logger.error(e)
        db.session.rollback()

    return redirect(url_for("detector.index"))


def make_color(labels):
    # 枠線の色をランダムに決定
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in labels]
    color = random.choice(colors)
    return color


def make_line(result_image):
    # 枠線を作成
    line = round(0.002 * max(result_image.shape[0:2])) + 1
    return line


def draw_lines(c1, c2, result_image, line, color):
    # 四角形の枠線を画像に追記
    cv2.rectangle(result_image, c1, c2, color, thickness=line)
    return cv2


def draw_texts(result_image, line, c1, cv2, color, labels, label):
    # 検知したテキストラベルを画像に追記
    display_txt = f"{labels[label]}"
    font = max(line - 1, 1)
    t_size = cv2.getTextSize(display_txt, 0, fontScale=line / 3, thickness=font)[0]
    c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
    cv2.rectangle(result_image, c1, c2, color, -1)
    cv2.putText(
        result_image,
        display_txt,
        (c1[0], c1[1] - 2),
        0,
        line / 3,
        [225, 255, 255],
        thickness=font,
        lineType=cv2.LINE_AA,
    )
    return cv2


def save_detected_image_tags(user_image, tags, detected_image_file_name):
    # 検知後画像の保存先パスをDBに保存する
    user_image.image_withTag_path = detected_image_file_name

    # 検知フラグをTrueにする
    user_image.is_detected = True
    # 変換後の画像パス
    user_image.image_withTag_path = detected_image_file_name
    db.session.add(user_image)

    # user_images_tagsレコードを作成する
    for tag in tags:
        user_image_tag = UserImageTag(user_image_id=user_image.id, tag_name=tag)
        db.session.add(user_image_tag)
    
    db.session.commit()


def exec_detect(user_image, target_image_path):
    # ラベルの読み込み
    labels = current_app.config["LABELS"]

    # 画像の読み込み
    image = Image.open(target_image_path)

    # 画像データをテンソル型の数値データへ変換
    image_tensor = torchvision.transforms.functional.to_tensor(image)

    # 学習済みモデルの読み込み
    model_path = current_app.config["MODEL_PATH"]
    print(f"MODEL_PATH: {model_path}")
    model = torch.load(model_path)

    # モデルの推論モードに切り替え
    model = model.eval()

    # 推論の実行
    output = model([image_tensor])[0]
    tags = []
    result_image = np.array(image.copy())

    # 学習済みモデルが検知した各物体の分だけ画像に追記
    for box, label, score in zip(output["boxes"], output["labels"], output["scores"]):
        if score > 0.5 and labels[label] not in tags:
            print(f"score: {score}")
            print(f"label: {labels[label]}")
            # 枠線の色の決定
            color = make_color(labels)
            # 枠線の作成
            line = make_line(result_image)
            # 検知画像の枠線とテキストラベルの枠線の位置情報
            c1 = (int(box[0]), int(box[1]))
            c2 = (int(box[2]), int(box[3]))
            # 画像に枠線を追記
            cv2 = draw_lines(c1, c2, result_image, line, color)
            # 画像にテキストラベルを追記
            cv2 = draw_texts(result_image, line, c1, cv2, color, labels, label)
            tags.append(labels[label])

    # 検知後の画像ファイル名を生成する
    detected_image_file_name = str(uuid.uuid4()) + ".jpg"

    # 画像コピー先パスを取得する
    detected_image_file_path = str(
        Path(current_app.config["UPLOAD_FOLDER"], detected_image_file_name)
    )
    # 変換後の画像ファイルを保存先へコピーする
    cv2.imwrite(detected_image_file_path, cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))

    # データベースにタグと変換後の画像パス情報を保存する
    save_detected_image_tags(user_image, tags, detected_image_file_name)
    
    return tags, detected_image_file_name


@dt.route("/detect/<string:image_id>", methods=["POST"])
def detect(image_id):
    # user_imagesテーブルからレコードを取得する
    user_image = db.session.query(UserImage).filter(UserImage.id == image_id).first()
    if user_image is None:
        flash("物体検知対象の画像が存在しません。")
        return redirect(url_for("detector.index"))

    # 物体検知対象の画像パスを取得する
    target_image_path = Path(current_app.config["UPLOAD_FOLDER"], user_image.image_path)
    
    try:
        # 物体検知を実行してタグと変換後の画像パスを取得する
        tags, detected_image_file_name = exec_detect(user_image, target_image_path)
    
    except Exception as e:
        flash("物体検知処理でエラーが発生しました。")
        # ロールバックする
        db.session.rollback()
        # エラーログ出力
        current_app.logger.error(e)
        return redirect(url_for("detector.index"))
    return redirect(url_for("detector.index"))