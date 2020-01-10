from flask import render_template, flash, redirect, url_for, request, json
from app import app
from app.forms import CustomerSigninForm, CustomerSignupForm
from flask_mysqldb import MySQL


# MySQL configurations
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'WMS'
mysql = MySQL(app)

# Routing scheme via meta decorators. Declare @app.route(... route name ...), then it calles the function below it.
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/signin')
def signin():
    form = CustomerSigninForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.user.data, form.remember.data))
        return redirect(url_for('index'))
    return render_template('signin.html', title='Customer Log In Portal', form=form)


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
    

@app.route('/signup',methods=['GET', 'POST'])
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
         

       
        
