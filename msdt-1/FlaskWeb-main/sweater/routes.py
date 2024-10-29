from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sweater import app, db
from sweater.models import User, Task, UsersTask


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/all_history")
@login_required
def all_history():
    # Получение всех задач, отсортированных по статусу и дедлайну
    all_tasks = Task.query.order_by(Task.status).order_by(Task.deadline).all()
    return render_template('all_history.html', tasks=all_tasks)


@app.route("/change_task")
@login_required
def change_task():
    # Получение всех задач со статусом "В процессе"
    all_tasks = Task.query.filter_by(status='В процессе').all()
    return render_template('change_task.html', tasks=all_tasks)


@app.route("/edit_task/<int:task_id>", methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)

    # Получение новых данных для задачи
    new_name = request.form.get('name')
    new_description = request.form.get('description')
    new_deadline = request.form.get('deadline')

    # Получение всех работников
    workers = User.query.filter_by(role='worker').all()
    user_ids = request.form.getlist('user_ids')

    if request.method == 'POST':
        # Проверка введенных данных
        if not new_name.strip():
            flash('Название не может быть пустым')
        elif not new_description.strip():
            flash('Описание не может быть пустым')
        elif len(user_ids) == 0:
            flash('У задания должны быть исполнители')
        elif datetime.strptime(new_deadline, '%Y-%m-%dT%H:%M') <= datetime.now().replace(microsecond=0):
            flash('Дедлайн не может быть таким')
        elif not new_deadline.strip():
            flash('Дедлайн не может быть пустым')
        else:
            # Удаление старых исполнителей и добавление новых
            UsersTask.query.filter_by(task_id=task_id).delete()
            for user_id in user_ids:
                new_user_task = UsersTask(user_id=user_id, task_id=task_id)
                db.session.add(new_user_task)

            # Обновление данных задачи
            task.name = new_name
            task.description = new_description
            task.start_date = datetime.now().replace(microsecond=0)
            task.deadline = new_deadline
            task.category_id = request.form.get('category_id')
            db.session.commit()  # Сохранение изменений
            return redirect(url_for('all_history'))

    return render_template('edit_task.html', task=task, users=workers)


@app.route("/create_task", methods=['POST', 'GET'])
@login_required
def create_task():
    # Получение данных для новой задачи
    name = request.form.get('name')
    description = request.form.get('description')
    start_date = datetime.now().replace(microsecond=0)
    deadline = request.form.get('deadline')
    status = 'В процессе'
    category_id = request.form.get('category_id')

    workers = User.query.filter_by(role='worker').all()
    user_ids = request.form.getlist('user_ids')

    if request.method == 'POST':
        # Проверка введенных данных
        if not name.strip():
            flash('Название не может быть пустым')
        elif not deadline.strip():
            flash('Дедлайн не может быть пустым')
        elif datetime.strptime(deadline, '%Y-%m-%dT%H:%M') <= datetime.now().replace(microsecond=0):
            flash('Дедлайн не может быть таким')
        elif len(user_ids) == 0:
            flash('У задания должны быть исполнители')
        elif not description.strip():
            flash('Описание не может быть пустым')
        else:
            # Создание новой задачи
            new_task = Task(name=name, description=description, start_date=start_date, deadline=deadline, status=status,
                            category_id=category_id)
            db.session.add(new_task)
            db.session.commit()  # Сохранение новой задачи

            # Привязка исполнителей к задаче
            for user_id in user_ids:
                new_user_task = UsersTask(user_id=int(user_id), task_id=new_task.task_id)
                db.session.add(new_user_task)
            db.session.commit()  # Сохранение привязок

            return redirect(url_for('all_history'))

    return render_template('create_task.html', users=workers)


@app.route("/tasks")
@login_required
def tasks():
    # Получение задач текущего пользователя со статусом "В процессе"
    user_tasks = current_user.users_tasks
    in_progress_tasks = [user_task.task for user_task in user_tasks if user_task.task.status == 'В процессе']
    in_progress_tasks.sort(key=lambda task: task.deadline)  # Сортировка по дедлайну
    return render_template('tasks.html', tasks=in_progress_tasks)


@app.route("/complete_task/<int:task_id>", methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        # Изменение статуса задачи на "Выполнено"
        task.status = 'Выполнено'
        task.end_date = datetime.now().replace(microsecond=0)
        db.session.commit()  # Сохранение изменений
        return jsonify({'message': 'Задача успешно выполнена'}), 200
    else:
        return jsonify({'error': 'Задача не найдена'}), 404


@app.route("/history")
@login_required
def history():
    # Получение задач текущего пользователя со статусами "Выполнено" и "Невыполнено"
    user_tasks = current_user.users_tasks
    two_status_tasks = [user_task.task for user_task in user_tasks if
                        user_task.task.status in ['Выполнено', 'Невыполнено']]
    two_status_tasks.sort(key=lambda task: (task.status != 'Невыполнено', task.status))  # Сортировка
    return render_template('history.html', tasks=two_status_tasks)


@app.route("/user_stat")
@login_required
def user_stat():
    # Получение статистики пользователей
    users = User.query.filter_by(role='worker').all()
    user_stats = []
    for user in users:
        user_stat2 = {
            'login': user.login,
            'rating': user.calculate_rating(),
            'completed_tasks': len([task for task in user.users_tasks if task.task.status == 'Выполнено']),
            'failed_tasks': len([task for task in user.users_tasks if task.task.status == 'Невыполнено']),
            'in_progress_tasks': len([task for task in user.users_tasks if task.task.status == 'В процессе'])
        }
        user_stats.append(user_stat2)

    sorted_user_stats = sorted(user_stats, key=lambda x: x['rating'], reverse=True)  # Сортировка по рейтингу
    return render_template('user_stat.html', user_stats=sorted_user_stats)


@app.route("/login", methods=['POST', 'GET'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            # Редирект в зависимости от роли пользователя
            if user.role == 'worker':
                return redirect(url_for('tasks'))
            elif user.role == 'moderator':
                return redirect(url_for('all_history'))
        else:
            flash('Логин или пароль неверны')
    else:
        flash('Введите логин и пароль')

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()  # Выход пользователя
    return redirect(url_for('home'))


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    role = request.form.get('role')

    if request.method == 'POST':
        # Проверка введенных данных
        if not login.strip():
            flash('Логин не может быть пустым')
        elif not password.strip():
            flash('Пароль не может быть пустым')
        elif password != password2:
            flash('Неправильно введен пароль')
        elif User.query.filter_by(login=login).first():
            flash('Пользователь с таким логином уже существует')
        else:
            # Хеширование пароля и создание нового пользователя
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd, role=role)
            db.session.add(new_user)
            db.session.commit()  # Сохранение нового пользователя
            return redirect(url_for('login_page'))

    return render_template('registration.html')


@app.route("/error")
def error():
    return render_template('error.html')
