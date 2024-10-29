from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from sweater.tasks import check_deadlines  # Импорт задачи проверки дедлайнов

# Инициализация приложения Flask
app = Flask(__name__)
app.secret_key = 'Danila'  # Секретный ключ для сессий
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:Jomangos123@localhost:1234/web'  # URI базы данных

# Инициализация расширений
db = SQLAlchemy(app)  # Инициализация SQLAlchemy
manager = LoginManager(app)  # Инициализация менеджера аутентификации


# Настройка APScheduler
class Config:
    SCHEDULER_API_ENABLED = True  # Включение API для планировщика

app.config.from_object(Config())
scheduler = APScheduler()  # Инициализация планировщика задач
scheduler.init_app(app)  # Привязка планировщика к приложению
scheduler.start()  # Запуск планировщика

# Добавление задачи в планировщик
scheduler.add_job(id='check_deadlines',
                  func=check_deadlines,
                  trigger='interval',
                  seconds=20)  # Задача будет выполняться каждые 20 секунд