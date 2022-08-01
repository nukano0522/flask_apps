import uuid
from pathlib import Path
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

from .forms import UploadImageForm, DeleteForm

from .models import UserImage
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

    delete_form = DeleteForm()

    return render_template(
        "detector/index.html", 
        user_images=user_images,
        delete_form = delete_form
    )


@dt.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@dt.route("/upload", methods=["GET", "POST"])
# ログイン必須とする
# @login_required
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
# @login_required
def delete_image(image_id):
    try:
        # user_image_tagsテーブルからレコードを削除する
        # db.session.query(UserImageTag).filter(
        #     UserImageTag.user_image_id == image_id
        # ).delete()

        # imageフォルダのファイルも削除する
        delete_image = db.session.query(UserImage).filter(UserImage.id == image_id).first()
        delete_image_path = Path(current_app.config["UPLOAD_FOLDER"], delete_image.image_path)
        os.remove(delete_image_path)

        # user_imageテーブルからレコードを削除する
        db.session.query(UserImage).filter(UserImage.id == image_id).delete()
        db.session.commit()
    except Exception as e:
        flash("画像削除処理でエラーが発生しました。")
        # エラーログ出力
        current_app.logger.error(e)
        db.session.rollback()
    return redirect(url_for("detector.index"))