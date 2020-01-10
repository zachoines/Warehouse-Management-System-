from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class CustomerSigninForm(FlaskForm):
    
    # validators is used to forced required behaviors to HTML form elements
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    signin = SubmitField('Sign In')