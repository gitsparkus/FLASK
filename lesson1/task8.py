"""
1) Задача 8.
Создать базовый шаблон для всего сайта, содержащий общие элементы дизайна (шапка, меню, подвал), и дочерние шаблоны для каждой отдельной страницы.
Например, создать страницу "О нас" и "Контакты", используя базовый шаблон.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def html_index():
    return render_template('task8/index.html')


@app.route('/about/')
def about():
    return render_template('task8/about.html')


@app.route('/contacts/')
def contacts():
    context = {
        'name': 'Имя',
        'phone': '898',
        'email': 'a@a.ru'
    }
    return render_template('task8/contacts.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
