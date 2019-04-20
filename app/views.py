from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
from app import app, db
from app.models import User


@app.route('/')
@app.route('/home')
def home():
    """Renders the top page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/thingstodo')
def ttd():
    return render_template(
        'thingstodo.html',
        title='Things To Do',
        year=datetime.now().year)


@app.route('/beautyandspa')
def bas():
    return render_template(
        'beauty.html',
        title='Beauty And Spa',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/local')
def loc():
    return render_template(
        'local.html',
        title='Local',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/goods')
def goo():
    """Renders the goods page."""
    return render_template(
        'goods.html',
        title='Goods',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/staffpicks')
def stp():
    """Renders the  page."""
    return render_template(
        'staffpicks.html',
        title='Staffs Pick Up',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/shoppingcart')
def cart():
    return render_template('cart.html')


@app.route('/delete')
def delete_item():
    return render_template('delete.html')


@app.route('/additem')
def add_item():
    return render_template('create.html')


@app.route('/edit/<pk>')
def edit_item(pk):
    return render_template('edit.html')


@app.route('/delete/<pk>')
def delete(pk):
    return redirect(url_for('home'))


@app.route('/view/<pk>')
def view(pk):
    return render_template('view.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
