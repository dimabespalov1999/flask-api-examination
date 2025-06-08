from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных окуржения
db = SQLAlchemy()  # Создание глобального объекта SQLAlchemy


# Функция по созданию фласк приложения возвращает объект приложения app
def create_app(test_config=None):

    app = Flask(__name__)  # Создание экземпляра Flask приложения

    # Конфигурация подключения к базе данных Postgresql
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        app.config.update(test_config)

    db.init_app(app)

    # Создание таблиц если оне не созданы
    with app.app_context():
        db.create_all()

    return app
