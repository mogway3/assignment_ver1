from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), index=True, unique=True)
    role_user = db.relationship('User', backref='roleuser', lazy="dynamic")

    def __repr__(self):
        return '<role {}>'.format(self.role_name)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    permission = db.Column(db.Integer, db.ForeignKey('role.id'), default=2)
    useraddress = db.relationship('Address', backref='useraddress', lazy="dynamic")
    shoppingrecord = db.relationship('Log', backref='shoppingrecord', lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# user no address
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    address = db.Column(db.String(200), nullable=False, index=True)
    contact = db.Column(db.Integer, nullable=False, index=True)

    def __repr__(self):
        return '<address {}>'.format(self.address)


# Shouhin no shurui
class Type(db.Model):
    __tablename__ = 'type'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(60), nullable=False, index=True)
    subcategoriestype = db.relationship('Subcategories', backref='Item type', lazy="dynamic")


def __repr__(self):
    return '<item type {}>'.format(self.address)


# shouhin category table
class Subcategories(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey('type.id'))
    name = db.Column(db.String(120), index=True, unique=True)
    acategories = db.relationship('Categories', backref='Sub_categories', lazy="dynamic")

    def __repr__(self):
        return '<sub category {}>'.format(self.name)


# shouhin category fuzoku table
class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    subcategory = db.Column(db.Integer, db.ForeignKey('subcategories.id'))
    name = db.Column(db.String(120), index=True, unique=True)
    item = db.relationship('Item', backref='Item Categories', lazy="dynamic")

    def __repr__(self):
        return '<category {}>'.format(self.name)


# shouhin shousai table
class Item(db.Model):
    __tablename__ = 'all_items'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    item_name = db.Column(db.String(120), index=True, unique=True)
    original_price = db.Column(db.Integer, index=True)
    discount_price = db.Column(db.Integer, index=True)
    created_at = db.Column('created', db.DateTime, default=datetime.utcnow)
    updated_at = db.Column('modified', db.DateTime, default=datetime.utcnow)
    location = db.relationship('Location', backref='Company Location', lazy="dynamic")
    detail = db.relationship('Detail', backref='Item Detail', lazy="dynamic")
    Logs = db.relationship('Log', backref='Item Name', lazy="dynamic")

    def __repr__(self):
        return '<items {}>'.format(self.item_name)


class Detail(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, db.ForeignKey('all_items.id'))
    detail_body = db.Column(db.String(200), nullable=False, index=True)
    detail_img = db.Column(db.String(200), index=True)

    def __repr__(self):
        return '<detail {}>'.format(self.detail_body)


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, db.ForeignKey('all_items.id'))
    location_name = db.Column(db.String(120), index=True, unique=True)
    region = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<location {}>'.format(self.location_name)


class Option(db.Model):
    __tablename__ = 'option'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, db.ForeignKey('all_items.id'))
    body = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<option {}>'.format(self.body)


class Log(db.Model):
    __tablename__ = 'ShoppingList'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('all_items.id'))
    buy_at = db.Column('Bought at', db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<bought  {}>'.format(self.buy_at)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(140))
    body = db.Column(db.String(200), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<comment {}>'.format(self.body)


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(140), nullable=False)
    company_type = db.Column(db.String(140))
    promotion = db.relationship('Promo', backref='companypr', lazy='dynamic')


class Promo(db.Model):
    __tablename__ = 'promo'
    id = db.Column(db.Integer, primary_key=True)
    starttime = db.Column(db.DateTime, default=datetime.utcnow)
    endtime = db.Column(db.DateTime)
    promoimg = db.Column(db.String(120))
    companyname = db.Column(db.String(140), db.ForeignKey('company.company_name'))
