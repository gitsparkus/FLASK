"""
Создать страницу, на которой будет форма для ввода числа
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с результатом, где будет
выведено введенное число и его квадрат.
"""

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = int(request.form.get('number'))
        return render_template('./task7/result.html', number=number)

    return render_template('./task7/index.html')


if __name__ == '__main__':
    app.run(debug=True)
