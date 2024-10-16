from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.secret_key = 'Danila'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Jomangos123@localhost:1234/web'
db = SQLAlchemy(app)
manager = LoginManager(app)


# Настройка APScheduler
class Config:
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from sweater import models, routes
from sweater.tasks import check_deadlines  # Импортируем задачу

# Добавляем задачу в планировщик
scheduler.add_job(id='check_deadlines', func=check_deadlines, trigger='interval', seconds=20)
