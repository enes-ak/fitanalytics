from flask import Flask


def create_app():
    app = Flask(__name__)

    # SESSION için GEREKLİ
    app.secret_key = "fitanalytics_secret_key"

    from .routes import main
    app.register_blueprint(main)

    return app