from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, DataRequired


class RegForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    name = StringField('Name')


class GuestForm(FlaskForm):
    passport = StringField('Passport Number', validators=[DataRequired(), Length(min=5, max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(min=3, max=99)])
