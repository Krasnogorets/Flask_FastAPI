"""
Задание
Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.
"""
from hashlib import sha256

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask import Flask, request, render_template, redirect, flash, url_for
from task_01_3_key import key
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from models import db, Users
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
csrf = CSRFProtect(app)
db.init_app(app)


@app.cli.command("init-db")
def init_db1():
    db.create_all()
    print('OK')


@app.route('/')
def index():
    return 'start'



class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    user_secondname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        if Users.query.filter(Users.email == form.email.data).first():
            flash('Такой пользователь существует!', 'danger')
            return redirect(url_for('register'))
        else:
            user = Users(username=form.username.data, user_secondname=form.user_secondname.data,
                         email=form.email.data,
                         password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрированны!', 'success')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
