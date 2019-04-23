from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ItemForm,EditItemForm
from app import app, db
from app.models import User, Item, Detail, Promo, Address, Categories, Subcategories, Type


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
    item = db.session.query(Item.item_name, Item.original_price, Item.discount_price, Detail.detail_body,
                            Detail.detail_img, Detail.detail_thumb).outerjoin(Detail, Item.id == Detail.item). \
        outerjoin(Categories, Categories.id == Item.category_id).outerjoin(Subcategories,
                                                                           Subcategories.id == Categories.subcategory) \
        .outerjoin(Type, Type.id == Subcategories.type).filter(Type.id == 3).order_by(Item.id).all()
    promo = Promo.query.all()
    return render_template(
        'view.html',
        title='Things To Do',
        year=datetime.now().year,
        message='Your contact page.',item=item, promo=promo
    )


@app.route('/beautyandspa')
def bas():
    item = db.session.query(Item.item_name, Item.original_price, Item.discount_price, Detail.detail_body,
                            Detail.detail_img, Detail.detail_thumb).outerjoin(Detail, Item.id == Detail.item). \
        outerjoin(Categories, Categories.id == Item.category_id).outerjoin(Subcategories,
                                                                           Subcategories.id == Categories.subcategory) \
        .outerjoin(Type, Type.id == Subcategories.type).filter(Type.id == 2).order_by(Item.id).all()
    promo = Promo.query.all()
    return render_template(
        'view.html',
        title='Beauty And Spa',
        year=datetime.now().year,
        item=item, promo=promo
    )


@app.route('/local')
def loc():
    """Renders the locao page."""
    return render_template(
        'view.html',
        title='Local',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/goods')
def goo():
    item = db.session.query(Item.item_name, Item.original_price, Item.discount_price, Detail.detail_body,
                            Detail.detail_img, Detail.detail_thumb).outerjoin(Detail, Item.id == Detail.item). \
        outerjoin(Categories, Categories.id == Item.category_id).outerjoin(Subcategories,
                                                                           Subcategories.id == Categories.subcategory) \
        .outerjoin(Type, Type.id == Subcategories.type).filter(Type.id == 1).order_by(Item.id).all()
    promo = Promo.query.all()
    return render_template(
        'view.html',
        title='Goods',
        year=datetime.now().year,
        message='Your contact page.',
        item=item, promo=promo
    )

@app.route('/goods/mens')
def mens():
    item = db.session.query(Item.item_name, Item.original_price, Item.discount_price, Detail.detail_body,
                            Detail.detail_img, Detail.detail_thumb).outerjoin(Detail, Item.id == Detail.item). \
        outerjoin(Categories, Categories.id == Item.category_id).outerjoin(Subcategories,
                                                                           Subcategories.id == Categories.subcategory) \
        .filter(Subcategories.id == 7).order_by(Item.id).all()
    promo = Promo.query.all()
    return render_template(
        'view.html',
        title='Goods',
        year=datetime.now().year,
        message='Your contact page.',
        item=item, promo=promo
    )

@app.route('/goods/womens')
def womens():
    item = db.session.query(Item.item_name, Item.original_price, Item.discount_price, Detail.detail_body,
                            Detail.detail_img, Detail.detail_thumb).outerjoin(Detail, Item.id == Detail.item). \
        outerjoin(Categories, Categories.id == Item.category_id).outerjoin(Subcategories,
                                                                           Subcategories.id == Categories.subcategory) \
        .filter(Subcategories.id == 6).order_by(Item.id).all()
    promo = Promo.query.all()
    return render_template(
        'view.html',
        title='Goods',
        year=datetime.now().year,
        message='Your contact page.',
        item=item, promo=promo
    )

@app.route('/staffpicks')
def stp():
    item = db.session.query(Item.item_name, Item.original_price, Item.discount_price, Detail.detail_body,Detail.detail_img, Detail.detail_thumb).outerjoin(Detail, Item.id == Detail.item). outerjoin(Categories, Categories.id == Item.category_id).outerjoin(Subcategories,Subcategories.id == Categories.subcategory) .filter(Subcategories.id == 3).order_by(Item.id).all()
    promo = Promo.query.all()
    return render_template(
        'view.html',
        title='Staffs Pick Up',
        year=datetime.now().year,
        message='Your contact page.',
        item=item,promo=promo
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
    pro = (db.session.query(User.username, Address.address, Address.contact).outerjoin(Address,
                                                                                       Address.user_id == User.id).filter(
        User.username == username)).all()
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


@app.route('/item/<item_name>')
def page(item_name):
    it = Item.query.filter_by(item_name=item_name).first()
    data = (db.session.query(Detail.detail_body,Detail.detail_img, Detail.detail_thumb).outerjoin(Item, Detail.item == Item.id).filter(
        Item.item_name == item_name)).first()
    return render_template(
        'page.html',
        title=item_name,
        year=datetime.now().year,
        it=it,
        data=data
    )

@app.route('/delete/<item_name>', methods=['GET', 'POST'])
@login_required
def deleteitem(item_name):
    item = Item.query.filter_by(item_name=item_name).delete()
    db.session.commit()
    flash('Congratulations, you are delete the Item!')
    return redirect(url_for('Home'))
