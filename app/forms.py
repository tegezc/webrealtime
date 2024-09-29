from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CreateUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    hobby = StringField('Hobby', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Create User')

class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    stock = StringField('Stock', validators=[DataRequired()])
    submit = SubmitField('Add Product')
