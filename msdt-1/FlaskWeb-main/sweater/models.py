from flask_login import UserMixin

from sweater import db, manager


class Category(db.Model):
    __tablename__ = 'Category'

    category_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    complexity = db.Column(db.BigInteger, nullable=False)


class Task(db.Model):
    __tablename__ = 'Task'

    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.BigInteger, db.ForeignKey('Category.category_id'), nullable=False)

    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))


class User(db.Model, UserMixin):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)

    def __init__(self, login, password, role):
        self.login = login
        self.password = password
        self.role = role

    def get_id(self):
        return self.user_id

    def calculate_rating(self):
        completed_tasks = sum(
            task.task.category.complexity for task in self.users_tasks if task.task.status == 'Выполнено')
        failed_tasks = sum(
            task.task.category.complexity for task in self.users_tasks if task.task.status == 'Невыполнено')
        return completed_tasks - failed_tasks

    def __str__(self):
        return self.user_id + self.login


class UsersTask(db.Model):
    __tablename__ = 'UsersTask'

    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Task.task_id'), primary_key=True)

    user = db.relationship('User', backref=db.backref('users_tasks', lazy=True))
    task = db.relationship('Task', backref=db.backref('users_tasks', lazy=True))


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
