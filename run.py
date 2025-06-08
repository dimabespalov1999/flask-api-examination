from app import create_app
from app.routes import bp

app = create_app()  # Создание приложения
app.register_blueprint(bp)  # Регистрация блюпринта с роутами

# if __name__ == '__main__':
#     app.register_blueprint(bp) # Регистрация блюпринта с роутами
#     app.run(debug=True, host='0.0.0.0', port=5000) # запуск приложения
