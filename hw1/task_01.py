"""Создать базовый шаблон для интернет-магазина, содержащий общие элементы дизайна (шапка, меню, подвал), и дочерние
шаблоны для страниц категорий товаров и отдельных товаров. Например, создать страницы «Одежда», «Обувь» и «Куртка»,
используя базовый шаблон."""
import os

from flask import Flask
from flask import render_template

# static_path = os.path.join(os.getcwd(), '../static')

app = Flask(__name__)


@app.route('/')
@app.route('/main/')
def main():
    context = {'title': 'Главная',
               'content': "главная страница магазина",
               'btn': 'Start Now',
               'img_center': "../static/img/Image.svg"}
    return render_template('main.html', **context)


@app.route('/clothes/')
def clothes():
    context = {'title': 'Одежда',
               'content': "здесь представлены наши лучшие образцы одежды",
               'btn': 'Buy clothes',
               'img_center': "../static/img/9461.jpg"
               }
    return render_template('clothes.html', **context)


@app.route('/boots/')
def boots():
    context = {'title': 'Обувь',
               'content': "здесь представлены наши лучшие образцы обуви",
               'btn': 'Buy boots',
               'img_center': "../static/img/boots.jpg"}
    return render_template('boots.html', **context)


@app.route('/jacket/')
def jacket():
    context = {'title': 'Куртка',
               'content': "десь представлены наши лучшие образцы курток",
               'btn': 'Buy jacket',
               'img_center': "../static/img/jackets.jpg"}
    return render_template('jacket.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
