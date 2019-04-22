from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL
from wtforms.fields.html5 import DateTimeField
from app.models import User, Item


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ItemForm(FlaskForm):
    itemid=IntegerField('ItemId',validators=[DataRequired()])
    itemname = StringField('Itemname', validators=[DataRequired()])
    categories = SelectField('Catagories',coerce=int, validators=[DataRequired()])
    original = IntegerField('Original Price', validators=[DataRequired()])
    discount = IntegerField('Discount Price', validators=[DataRequired()])
    start = DateTimeField('Start Date', default=datetime.today)
    end = DateTimeField('End Date', default=datetime.today)
    detail = TextAreaField('Detail', validators=[DataRequired()])
    thumbnail = StringField('Thumbnail Link', validators=[DataRequired(), URL()])
    image = StringField('Image Link', validators=[DataRequired(), URL()])
    submit = SubmitField('ADD')

    def validate_itemname(self, itemname):
        item = Item.query.filter_by(item_name=itemname.data).first()
        if item is not None:
            raise ValidationError('Please use a different name.')

    def validate_itemid(self, itemid):
        itemid = Item.query.filter_by(id=itemid.data).first()
        if itemid is not None:
            raise ValidationError('Please use a different Number.')

    def validate_on_submit(self):
        result = super(ItemForm, self).validate()
        if (self.start.data > self.end.data):
            return False
        else:
            return result
