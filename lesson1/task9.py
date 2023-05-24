"""
2) Задача 9
Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал), и дочерние
шаблоны для страниц категорий товаров и отдельных товаров.
Например, создать страницы "Одежда", "Обувь" и "Куртка", используя базовый шаблон.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def html_index():
    return render_template('task9/index.html')


@app.route('/about/')
def about():
    return render_template('task9/about.html')


@app.route('/clothes/')
def clothes():
    context = [
        {'path': '/clothes/jacket/', 'name': 'Куртка'},
        {'path': '/clothes/jeans/', 'name': 'Джинсы'},
    ]
    return render_template('task9/clothes.html', clothes=context)


@app.route('/clothes/jacket/')
def jacket():
    context = {

        'img_src': '/static/image/jacket.jpg',
        'name': 'Обычная куртка',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos eos facere harum ipsa '
                       'maiores recusandae repellendus sit veniam? Architecto aut eaque inventore, maiores officia '
                       'tempora voluptate? Architecto asperiores culpa cum delectus dolorem earum enim error, esse, '
                       'hic ipsa, maiores possimus quas saepe sunt tenetur ullam voluptatibus? Aliquid facere iusto '
                       'molestias.'}
    return render_template('task9/clothes_item.html', **context)


@app.route('/clothes/jeans/')
def jeans():
    context = {
        'img_src': '/static/image/jeans.jpg',
        'name': 'Красивые джинсы',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Dignissimos eos facere harum ipsa '
                       'maiores recusandae repellendus sit veniam? Architecto aut eaque inventore, maiores officia '
                       'tempora voluptate? Architecto asperiores culpa cum delectus dolorem earum enim error, esse, '
                       'hic ipsa, maiores possimus quas saepe sunt tenetur ullam voluptatibus? Aliquid facere iusto '
                       'molestias.'}
    return render_template('task9/clothes_item.html', **context)


@app.route('/shoes/')
def shoes():
    return render_template('task9/shoes.html')


if __name__ == '__main__':
    app.run(debug=True)
