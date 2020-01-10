from flask import render_template, flash, redirect
from app import app
from app.forms import CustomerSigninForm

@app.route('/')

# Routing scheme via meta decorators. Declare @app.route(... route name ...), then it calles the function below it.
@app.route('/index')
def index():
    user = {'username': 'Zach Oines'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/signin')
def login():
    form = CustomerSigninForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('signin.html', title='Customer Log In Portal', form=form)