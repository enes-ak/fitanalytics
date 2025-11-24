# app/blueprints/__init__.py

from flask import Blueprint

main = Blueprint(
    "main",
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Route modüllerini import ettiğinde, decorator’lar otomatik olarak blueprint'e bağlanır.
# Import’lar fonksiyon içinde değil, direkt modül seviyesinde yapılmalı.
from . import api      # noqa
from . import auth     # noqa
from . import templates    # noqa
from . import workouts     # noqa
