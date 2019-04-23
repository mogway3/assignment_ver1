from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ItemForm
from app import app, db
from app.models import User, Item, Detail, Promo, Address, Categories


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/home')
def home():
    item = db.session.query(Item.item_name, Item.original_price, Item.discount_price, Detail.detail_body,
                            Detail.detail_img, Detail.detail_thumb).outerjoin(Detail, Item.id == Detail.item).order_by(
        Item.id).all()
    promo = Promo.query.all()
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        item=item, promo=promo)


@app.route('/thingstodo')
def ttd():
    """Renders the thingstodo page."""
    return render_template(
        'thingstodo.html',
        title='Things To Do',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/beautyandspa')
def bas():
    """Renders the beauty page."""
    return render_template(
        'beauty.html',
        title='Beauty And Spa',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/local')
def loc():
    """Renders the locao page."""
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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


@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    pro = Address.query.join(User).all()
    return render_template('profile.html', user=user, pro=pro)


@app.route('/newitem', methods=['GET', 'POST'])
@login_required
def newitem():
    catnow = db.session.query(Categories).all()
    cat = [(i.id, i.name) for i in catnow]
    form = ItemForm()
    form.categories.choices = cat
    if form.validate_on_submit():
        item = Item(id=form.itemid.data, item_name=form.itemname.data, category_id=form.categories.data,
                    original_price=form.original.data, discount_price=form.discount.data, created_at=form.start.data,
                    finish_at=form.end.data)
        db.session.add(item)
        detail = Detail(item=form.itemid.data, detail_body=form.detail.data, detail_img=form.image.data,
                        detail_thumb=form.thumbnail.data)
        db.session.add(detail)
        db.session.commit()
        flash('Congratulations, you are a new item')
        return redirect(url_for('home'))
    return render_template('create.html', title='Add new item', form=form)
