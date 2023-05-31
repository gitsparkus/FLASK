"""
Создать форму для регистрации пользователей на сайте. Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль"
и кнопку "Зарегистрироваться". При отправке формы данные должны сохраняться в базе данных, а пароль должен быть
зашифрован.
"""

import hashlib
from flask import Flask, request, render_template
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password = request.form.get('password')
        salted_password = password + email
        hashed_password = hashlib.md5(salted_password.encode()).hexdigest()

        user = User(username=name, usersurname=surname, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return repr(user)
    else:
        return render_template('./index.html')


if __name__ == '__main__':
    app.run(debug=True)
