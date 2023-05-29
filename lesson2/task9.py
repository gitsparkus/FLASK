"""
Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан
cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия, где будет
отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными
пользователя и произведено перенаправление на страницу ввода имени и электронной почты.
"""
from flask import Flask, request, render_template, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        response = make_response(redirect(url_for('hello')))
        response.set_cookie('name', name)
        response.set_cookie('email', email)

        return response

    if request.cookies.get('name'):
        return redirect(url_for('hello'))
    else:
        return render_template('./task9/index.html')


@app.route('/hello/')
def hello():
    name = request.cookies.get('name')

    return render_template('./task9/hello.html', name=name)


@app.post('/logout/')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('name')
    response.delete_cookie('email')

    return response


if __name__ == '__main__':
    app.run(debug=True)
