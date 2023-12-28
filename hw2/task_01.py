"""
Создать страницу, на которой будет форма для ввода имени
и электронной почты
При отправке которой будет создан cookie файл с данными
пользователя
Также будет произведено перенаправление на страницу
приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка "Выйти"
При нажатии на кнопку будет удален cookie файл с данными
пользователя и произведено перенаправление на страницу
ввода имени и электронной почты.
"""
from flask import Flask, request, render_template, redirect, url_for, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('task_09.html')


@app.post('/submit')
def submit():
    name = request.form['name']
    email = request.form['email']
    response = make_response(render_template('result3.html', name=name))
    response.set_cookie('username', name)
    response.set_cookie('email', email)
    return response


@app.post('/clear/')
def clear():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')
    response.delete_cookie('email')
    return response


if __name__ == '__main__':
    app.run(port=9000, debug=True)
