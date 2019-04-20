from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='role')
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), index=True, unique=True)
    permission = db.Column(db.String(50))

    def __repr__(self):
        return '<role {}>'.format(self.role_name)


class Home(db.Model):
    __tablename__ = 'home'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    item_name = db.Column(db.String(120), index=True, unique=True)
    original_price = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)
    categories = db.relationship('Categories', backref='categories')
    created_at = db.Column('created', db.DateTime, default=datetime.utcnow)
    updated_at = db.Column('modified', db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Home Improvement {}>'.format(self.item_name)


class Foods(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    item_name = db.Column(db.String(120), index=True, unique=True)
    original_price = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)
    categories = db.relationship('Categories', backref='categories')
    created_at = db.Column('created', db.DateTime, default=datetime.utcnow)
    updated_at = db.Column('modified', db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Foods {}>'.format(self.item_name)


class Toys(db.Model):
    __tablename__ = 'toys'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    item_name = db.Column(db.String(120), index=True, unique=True)
    original_price = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)
    categories = db.relationship('Categories', backref='categories')
    created_at = db.Column('created', db.DateTime, default=datetime.utcnow)
    updated_at = db.Column('modified', db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Toys {}>'.format(self.item_name)


class Entertainments(db.Model):
    __tablename__ = 'entertainments'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    item_name = db.Column(db.String(120), index=True, unique=True)
    original_price = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)
    categories = db.relationship('Categories', backref='categories')
    created_at = db.Column('created', db.DateTime, default=datetime.utcnow)
    updated_at = db.Column('modified', db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Entertainments {}>'.format(self.item_name)


class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    services_name = db.Column(db.String(120), index=True, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    original_price = db.Column(db.Integer)
    discount_price = db.Column(db.Integer)
    categories = db.relationship('Categories', backref='categories')
    location = db.relationship('Location', backref='location')
    created_at = db.Column('created', db.DateTime, default=datetime.utcnow)
    updated_at = db.Column('modified', db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<services {}>'.format(self.services_name)


class Subcategories(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<sub category {}>'.format(self.name)


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    type = db.Column(db.String(120))

    def __repr__(self):
        return '<category {}>'.format(self.name)


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), index=True, unique=True)
    region = db.Column(db.String(120))

    def __repr__(self):
        return '<location {}>'.format(self.location_name)


class Log(db.Model):
    __tablename__ = 'Shopping List'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    goods_name = db.Column(db.String(120))
    buy_at = db.Column('buy at', db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<bought  {}>'.format(self.buy_at)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(db.Integer, backref='User')

    def __repr__(self):
        return '<comment {}>'.format(self.body)
