from datetime import datetime
from sweater import db, scheduler
from sweater.models import Task
from pytz import timezone

# Определение локального часового пояса
local_tz = timezone('Europe/Samara')


def check_deadlines():
    # Создание контекста приложения для доступа к базе данных
    with scheduler.app.app_context():
        # Получение текущего времени в локальном часовом поясе
        now = datetime.now(local_tz).replace(microsecond=0)

        # Запрос задач с истекшими сроками, которые находятся в процессе выполнения
        tasks = Task.query.filter(Task.deadline < now, Task.status == 'В процессе').all()

        for task in tasks:
            # Обновление статуса задачи на "Невыполнено"
            task.status = 'Невыполнено'
            db.session.commit()  # Сохранение изменений в базе данных
