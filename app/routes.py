from flask import render_template, flash, redirect, url_for, request, json, session
from app import app
from app.forms import CustomerSigninForm, CustomerSignupForm
from flask_mysqldb import MySQL
from flask_login import current_user, LoginManager, UserMixin, login_required, logout_user, current_user, login_user

# Import Local classes
from app.classes.user import User


# MySQL configurations
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'WMS'
mysql = MySQL(app)

# User Authentication
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id=user_id, db=mysql)

# Routing scheme via meta decorators. Declare @app.route(... route name ...), then it calles the function below it.
@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return render_template('profile.html', accountInfo = { "name" : session['user name'], "email" : session['user email']})
    else:
        return render_template('index.html', title='Home')

@app.route('/showSignIn', methods=['GET', 'POST'])
def showSignIn():
    return render_template('signin.html')

@app.route('/signin', methods=['POST'])
def signin():
    form = CustomerSigninForm()
    if request.method == 'POST':
        
        print(form.errors)
        password=request.form['password']
        email=request.form['email']
        
        if email and password:
            
            user = User(email, password, mysql)
            login_user(user)
    
            if current_user.is_authenticated:
                session['logged_in'] = True
                session['user email'] = user.get_id() 
                session['user name'] = user.get_user_name()
                return render_template('profile.html', accountInfo = { "name" : user.get_user_name(), "email" : user.get_id()})

            else:
                session['logged_in'] = False
                return render_template('signin.html', form=form)
           

    

@app.route('/showSignUp', methods=['GET', 'POST'])
def showSignUp():
    return render_template('signup.html')
    

@app.route('/signup')
def signup():
    form = CustomerSigninForm(request.form)
    if request.method == 'POST':
        
        print(form.errors)
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        print(name +  " " + email + " " + password)
    
        # if form.validate():
        if name and email and password:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `wms`.`__user`(`user_name`, `user_username`, `user_password`) VALUES (%s, %s, %s)", (name, email, password))
            mysql.connection.commit()
            cur.close()

    return render_template('signin.html', form=form)

@app.route('/item_management/')
def dashboard():   
    if current_user.is_authenticated:
        return render_template('profile.html', accountInfo = { "name" : session['user name'], "email" : session['user email']})
    else:
        return render_template('index.html', title='Home')
         
@app.route('/item_management/<item_type>')
def manage_items(item_type):   
    items = None
    print(item_type)
    if item_type == 'product':  
        items = [
            {
                'ProductID': 1,
                'SKU': 123,
                'ProductDescription' : "A fine prodiuct"
            },
            {
                'ProductID': 2,
                'SKU': 321,
                'ProductDescription' : "Another fine prodiuct"
            }
        ]

    elif item_type == 'order':
        items = [
            {
                'ProductID': 1,
                'SKU': 123,
                'ProductDescription' : "A fine prodiuct"
            },
            {
                'ProductID': 2,
                'SKU': 321,
                'ProductDescription' : "Another fine prodiuct"
            }
        ]
        
    elif item_type == 'bin':
        items = [
            {
                'ProductID': 1,
                'SKU': 123,
                'ProductDescription' : "A fine prodiuct"
            },
            {
                'ProductID': 2,
                'SKU': 321,
                'ProductDescription' : "Another fine prodiuct"
            }
        ]
    
    elif item_type == 'order_line':
        items = [
            {
                'ProductID': 1,
                'SKU': 123,
                'ProductDescription' : "A fine prodiuct"
            },
            {
                'ProductID': 2,
                'SKU': 321,
                'ProductDescription' : "Another fine prodiuct"
            }
        ]
    
    elif item_type == 'inventory':
        items = [
            {
                'ProductID': 1,
                'SKU': 123,
                'ProductDescription' : "A fine prodiuct"
            },
            {
                'ProductID': 2,
                'SKU': 321,
                'ProductDescription' : "Another fine prodiuct"
            }
        ]
    
    return render_template('adjust_items.html', products=items, itemType=item_type, accountInfo = { "name" : session['user name'], "email" : session['user email'] })
        

