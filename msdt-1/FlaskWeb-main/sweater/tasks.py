from datetime import datetime
from sweater import db, scheduler
from sweater.models import Task
from pytz import timezone

local_tz = timezone('Europe/Samara')


def check_deadlines():
    with scheduler.app.app_context():
        now = datetime.now(local_tz).replace(microsecond=0)
        tasks = Task.query.filter(Task.deadline < now, Task.status == 'В процессе').all()
        for task in tasks:
            task.status = 'Невыполнено'
            db.session.commit()
