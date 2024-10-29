from flask_login import UserMixin
from sweater import db, manager

class Category(db.Model):
    __tablename__ = 'Category'

    category_id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор категории
    description = db.Column(db.Text, nullable=False)        # Описание категории
    complexity = db.Column(db.BigInteger, nullable=False)   # Сложность категории

class Task(db.Model):
    __tablename__ = 'Task'

    task_id = db.Column(db.Integer, primary_key=True)      # Уникальный идентификатор задачи
    name = db.Column(db.Text, nullable=False)               # Название задачи
    description = db.Column(db.Text)                        # Описание задачи
    start_date = db.Column(db.DateTime, nullable=False)    # Дата начала задачи
    end_date = db.Column(db.DateTime)                       # Дата окончания задачи
    deadline = db.Column(db.DateTime, nullable=False)      # Дедлайн задачи
    status = db.Column(db.Text, nullable=False)             # Статус задачи
    category_id = db.Column(db.BigInteger, db.ForeignKey('Category.category_id'), nullable=False)  # Ссылка на категорию

    # Связь с моделью Category
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))

class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)      # Уникальный идентификатор пользователя
    login = db.Column(db.Text, nullable=False, unique=True)  # Логин пользователя
    password = db.Column(db.Text, nullable=False)            # Хэшированный пароль
    role = db.Column(db.Text, nullable=False)                # Роль пользователя (например, работник или модератор)

    def __init__(self, login, password, role):
        self.login = login
        self.password = password
        self.role = role

    def get_id(self):
        return self.user_id

    def calculate_rating(self):
        # Подсчет рейтинга пользователя на основе завершенных и не завершенных задач
        completed_tasks = sum(
            task.task.category.complexity for task in self.users_tasks if task.task.status == 'Выполнено'
        )
        failed_tasks = sum(
            task.task.category.complexity for task in self.users_tasks if task.task.status == 'Невыполнено'
        )
        return completed_tasks - failed_tasks

    def __str__(self):
        return f"{self.user_id} - {self.login}"

class UsersTask(db.Model):
    __tablename__ = 'UsersTask'

    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)  # Ссылка на пользователя
    task_id = db.Column(db.Integer, db.ForeignKey('Task.task_id'), primary_key=True)    # Ссылка на задачу

    # Связи с пользователем и задачей
    user = db.relationship('User', backref=db.backref('users_tasks', lazy=True))
    task = db.relationship('Task', backref=db.backref('users_tasks', lazy=True))

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)  # Загрузка пользователя по идентификатору
