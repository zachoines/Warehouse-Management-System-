from flask_wtf import FlaskForm
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, PasswordField, BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

class CustomerSigninForm(FlaskForm):
    
    # validators is used to forced required behaviors to HTML form elements
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    signin = SubmitField('Sign In')


class CustomerSignupForm(FlaskForm):
    
    # validators is used to forced required behaviors to HTML form elements
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    signup = SubmitField('Sign up')

    