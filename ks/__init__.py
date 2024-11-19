from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Создаем объект для работы с базой данных

def create_app():
    app = Flask(__name__)  # Создаем Flask приложение
    app.config.from_object('config.Config')  # Загружаем конфигурацию из config.py

    db.init_app(app)  # Инициализируем объект базы данных с приложением

    # Импортируем и регистрируем Blueprint для API
    from .api import api
    app.register_blueprint(api, url_prefix='/api')  # Регистрируем Blueprint api

    return app
