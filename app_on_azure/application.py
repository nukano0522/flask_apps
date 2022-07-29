import logging
import os

from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

app = Flask(__name__)

# SECRET_KEYを追加する
# app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
app.config["SECRET_KEY"] = "aaa"

# ログレベルを設定する
app.logger.setLevel(logging.DEBUG)

# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Mailクラスのコンフィグを追加する
# app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
# app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
# app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
# app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
# app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
# app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# 本番（AzureWebApp）だと環境変数が取得できていないのでハードコーディング
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "testforwebapi@gmail.com"
app.config["MAIL_PASSWORD"] = "udpltmsfvoemhxmd"
app.config["MAIL_DEFAULT_SENDER"] = "MailForWebAPI"

# DebugToolbarExtensionにアプリケーションをセットする
toolbar = DebugToolbarExtension(app)

# flask-mail拡張を登録する
mail = Mail(app)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":

        # form属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 入力チェック
        is_valid = True
        if not username:
            flash("ユーザ名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # メールを送る
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )

        # 問い合わせ完了エンドポイントへリダイレクトする
        flash("問い合わせ内容はメールにて送信しました。問い合わせありがとうございます。")

        # contactエンドポイントへリダイレクトする
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    # msg = Message(subject, sender=app.config["MAIL_DEFAULT_SENDER"], recipients=[to])
    msg = Message(subject, sender="MailForWebAPI", recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


# 実行
if __name__ == "__main__":
    app.run(debug=True)
