from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, DeleteForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app import db


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("login page")
    if current_user.is_authenticated:
        print('user authenticated')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # user is None refers to username is not in the database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # add user into memory session from database
        print("adding user into memory session from database...")
        # This would change current_user.is_authenticated to be true
        # This would trigger load_user in models.py
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# login-required forces user to log in first; if user go to /index without log in, flask would go to login?next=/index
@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Adam'},
            'body': 'Today is raining!'
        },
        {
            'author': {'username': 'Bob'},
            'body': 'I like the movie.'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/logout')
def logout():
    # change current_user.is_authenticated to false
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/deleteuser', methods=['GET', 'POST'])
def deleteuser():
    form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # user is None refers to username is not in the database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('deleteuser'))
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted from database successfully!')
        return redirect(url_for('login'))
    return render_template('delete.html', title='Delete', form=form)


@app.route('/user/<username>') # dynamic variable, <> means that it can be any value
@login_required
def user(username):
    # dynamic variable in URI will be parsed as inputs to user
    # provided by SQLAlchemy, if user is not in the db, it will return 404
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
