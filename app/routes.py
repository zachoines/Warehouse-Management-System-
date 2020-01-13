# Import Server, routing, and database classes
from flask import render_template, flash, redirect, url_for, request, json, session
from app import app
from app.forms import CustomerSigninForm, CustomerSignupForm, ProductCreateform
from flask_mysqldb import MySQL
from flask_login import current_user, LoginManager, UserMixin, login_required, logout_user, current_user, login_user

# Import Local classes
from app.classes.user import User
from app.classes.product import Product
from app.classes.order import Order
from app.classes.orderLine import OrderLine
from app.classes.bin import Bin
from app.classes.inventory import Inventory


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

# Utility Functions
def count(table):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM " + "`wms`.`_" + table + "`", [])
    ((response,),) = cur.fetchall()
    return response

def database_counts():
    bins = count('bins')
    inventory = count("inventory")
    orders = count("order")
    orderlines = count("orderlines")
    products = count("product")

    updated_counts = {
        "bins" : bins,
        "inventory" : inventory,
        "orders" : orders,
        "orderlines" : orderlines,
        "products" : products
    }

    session['counts'] = updated_counts

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id=user_id, db=mysql)

# Routing scheme via meta decorators. Declare @app.route(... route name ...), then it calles the function below it.
@app.route('/')
@app.route('/index')
def index():
    database_counts()
    if current_user.is_authenticated:
        return render_template('account_management.html', accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
    else:
        return render_template('index.html', title='Home')

@app.route('/showSignIn', methods=['GET', 'POST'])
def showSignIn():
    return render_template('signin.html')

@app.route('/signOut', methods=['GET', 'POST'])
def signOut():
    logout_user()
    return render_template('signin.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = CustomerSigninForm()
    if request.method == 'POST':
        
        password=request.form['password']
        email=request.form['email']
        
        if email and password:
            user = User(email, password, mysql)
            if user.authenticated:
                login_user(user)
                session['logged_in'] = True
                session['user email'] = user.get_id() 
                session['user name'] = user.get_user_name()
                return render_template('account_management.html', accountInfo = { "name" : user.get_user_name(), "email" : user.get_id(), "counts" : session['counts']})

            else:
                session['logged_in'] = False
                return render_template('signin.html', form=form)
    else:
        session['logged_in'] = False
        return render_template('signin.html', form=form)
           
    
# Called return sign up page
@app.route('/showSignUp', methods=['GET'])
def showSignUp():
    return render_template('signup.html')
    

# Called to return sign in page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CustomerSigninForm(request.form)
    if request.method == 'POST':
        
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']

        if name and email and password:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `wms`.`__user`(`user_name`, `user_username`, `user_password`) VALUES (%s, %s, %s)", (name, email, password))
            mysql.connection.commit()
            cur.close()

    return render_template('signin.html', form=form)

# This is the main user portal
@app.route('/item_management/', methods=['GET'])
def dashboard():   
    database_counts()
    if current_user.is_authenticated:
        return render_template('account_management.html', accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
    else:
        return render_template('index.html', title='Home')
         
@app.route('/item_management/<item_type>/<action_type>/')
def itemAction(item_type, action_type): 
    items = []
    if item_type == 'product':  

        if action_type == 'create':  
            return render_template('actions/product_create.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})

        elif action_type == 'edit':
            return render_template('actions/product_edit.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
            
        elif action_type == 'delete':
            return render_template('actions/product_delete.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
        
        elif action_type == 'view':

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM `wms`.`_product`")
            response = cur.fetchall()
            for item in response:
                items.append(Product(*item))

            return render_template('actions/product_view.html', products=items, itemType=item_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})

    elif item_type == 'order':
        if action_type == 'create':  
            return render_template('actions/order_create.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})

        elif action_type == 'edit':
            return render_template('actions/order_edit.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
            
        elif action_type == 'delete':
            return render_template('actions/order_delete.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
        
        elif action_type == 'view':

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM `wms`.`_order`")
            response = cur.fetchall()
            for (OrderID, OrderNumber, DateOrdered, CustomerName, CustomerAddress) in response:
                items.append(Order(OrderID, OrderNumber, DateOrdered.date(), CustomerName, CustomerAddress))

            return render_template('actions/order_view.html', products=items, itemType=item_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
            
    elif item_type == 'bin':
        if action_type == 'create':  
            return render_template('actions/bin_create.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})

        elif action_type == 'edit':
            return render_template('actions/bin_edit.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
            
        elif action_type == 'delete':
            return render_template('actions/bin_delete.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'] , "counts" : session['counts']})
        
        elif action_type == 'view':

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM `wms`.`_bins`")
            response = cur.fetchall()
            for item in response:
                items.append(Bin(*item))

            return render_template('actions/bin_view.html', products=items, itemType=item_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
    
    elif item_type == 'order_lines':
        if action_type == 'create':  
            return render_template('actions/order_line_create.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})

        elif action_type == 'edit':
            return render_template('actions/order_line_edit.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
            
        elif action_type == 'delete':
            return render_template('actions/order_line_delete.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'] , "counts" : session['counts']})
        
        elif action_type == 'view':

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM `wms`.`_orderlines`")
            response = cur.fetchall()
            for item in response:
                print(item)
                items.append(OrderLine(*item))

            return render_template('actions/inventory_view.html', products=items, itemType=item_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
    
    elif item_type == 'inventory':
        if action_type == 'create':  
            print("here we are")
            return render_template('actions/inventory_create.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})

        elif action_type == 'edit':
            return render_template('actions/inventory_edit.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
            
        elif action_type == 'delete':
            return render_template('actions/inventory_delete.html', itemType = item_type, actionType = action_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
        
        elif action_type == 'view':
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM `wms`.`_inventory`")
            response = cur.fetchall()
            for item in response:
                items.append(Inventory(*item))

            return render_template('actions/inventory_view.html', products=items, itemType=item_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})
    return render_template('actions/product_view.html', products=items, itemType=item_type, accountInfo = { "name" : session['user name'], "email" : session['user email'], "counts" : session['counts']})

# Functions for inventory event interception
@app.route('/item_management/product/create/execute', methods = ['POST'])
def productCreate():
    sku = request.form.get('sku')
    product_description = request.form.get('product_description')

    try:
        if sku and product_description:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `wms`.`_product`(`SKU`, `ProductDescription`) VALUES (%s, %s)", (sku, product_description)) 
            mysql.connection.commit()
            cur.close()   
    except:
        print("Error creating product.")
    finally:   
        return redirect(url_for("index"))
    

    
    
@app.route('/item_management/product/edit/execute', methods = ['POST'])
def productEdit():
    product_id = request.form.get('product_id')
    sku = request.form.get('sku')
    product_description = request.form.get('product_description')

    try:
        if product_id and sku and product_description:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE `wms`.`_product` SET `SKU` = (%s), `ProductDescription` = (%s) WHERE `ProductID` = (%s)", (sku, product_description, product_id))
            mysql.connection.commit()
            ur.close()
    except:
        print("Error editing product.")
    finally:
        return redirect(url_for("index")) 

@app.route('/item_management/product/delete/execute', methods = ['POST'])
def productDelete():

    sku = request.form.get('sku')

    try:
        if sku:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM `wms`.`_product` WHERE `SKU` = %s", [sku])
            mysql.connection.commit()   
            cur.close()       
    except:
        print("Error deleting product.")
    finally:
        return redirect(url_for("index"))

@app.route('/item_management/order/create/execute', methods = ['POST'])
def orderCreate():

    OrderNumber = request.form.get('OrderNumber')
    DateOrdered = request.form.get('DateOrdered')
    CustomerName = request.form.get('CustomerName')
    CustomerAddress = request.form.get('CustomerAddress')

    try:
        if OrderNumber and DateOrdered and CustomerName and CustomerAddress:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `wms`.`_order`( `OrderNumber`, `DateOrdered`, `CustomerName`, `CustomerAddress`) VALUES (%s, %s, %s, %s)", (OrderNumber, DateOrdered, CustomerName, CustomerAddress))
            mysql.connection.commit()
            cur.close()
           
    except expression as identifier:
        print("Error creating order.")
    finally:
        return redirect(url_for("index"))

    

    

@app.route('/item_management/order/edit/execute', methods = ['POST'])
def orderEdit():
    OrderNumber = request.form.get('OrderNumber')
    DateOrdered = request.form.get('DateOrdered')
    CustomerName = request.form.get('CustomerName')
    CustomerAddress = request.form.get('CustomerAddress')

    try:
        if OrderNumber and DateOrdered and CustomerName and CustomerAddress:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE `wms`.`_order` SET `DateOrdered` = (%s), `CustomerName` = (%s), `CustomerAddress` = (%s) WHERE `OrderNumber` = (%s)", (DateOrdered, CustomerName, CustomerAddress, OrderNumber))
            mysql.connection.commit()
            cur.close()
            
    except:
        print("Error editing order.")
    finally:  
        return redirect(url_for("index"))

    

    

@app.route('/item_management/order/delete/execute', methods = ['POST'])
def orderDelete():
    OrderNumber = request.form.get('OrderNumber')

    try:
        if OrderNumber:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM `wms`.`_order` WHERE `OrderNumber` = %s", [OrderNumber])
            mysql.connection.commit()
            cur.close()
            
    except:
        print('Error deleting order number.')
    finally:
        return redirect(url_for("index"))

    
@app.route('/item_management/order_line/create/execute', methods = ['POST'])
def orderLineCreate():

    OrderID = request.form.get('OrderID')
    ProductID = request.form.get('ProductID')
    QTY = request.form.get('QTY')

    try:
        if OrderID and ProductID and QTY:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `wms`.`_orderlines`( `OrderID`, `ProductID`, `QTY`) VALUES (%s, %s, %s)", (OrderID, ProductID, QTY))
            mysql.connection.commit()   
            cur.close()      
    except:
        print("Error creating order line")
    finally:
        return redirect(url_for("index"))   

@app.route('/item_management/order_line/edit/execute', methods = ['POST'])
def orderLineEdit():
    OrderLineID = request.form.get('OrderLineID')
    OrderID = request.form.get('OrderID')
    ProductID = request.form.get('ProductID')
    QTY = request.form.get('QTY')

    try:
        if OrderLineID and OrderID and ProductID and QTY:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE `wms`.`_orderlines` SET `OrderID` = (%s), `ProductID` = (%s), `QTY` = (%s) WHERE `OrderLineID` = (%s)", (OrderID, ProductID, QTY, OrderLineID))
            mysql.connection.commit()     
            cur.close()     
    except:
        print("Error executing order line edit")
    finally:
        return redirect(url_for("index"))

    

    

@app.route('/item_management/order_line/delete/execute', methods = ['POST'])
def orderLineDelete():
    OrderLineID = request.form.get('OrderLineID')

    try:
        if OrderLineID:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM `wms`.`_orderlines` WHERE `OrderLineID` = %s", [OrderLineID])
            mysql.connection.commit()
            cur.close()           
    except:
        print("Error executing order line delete.")
    finally: 
        return redirect(url_for("index"))

@app.route('/item_management/bin/create/execute', methods = ['POST'])
def binCreate():

    BinName = request.form.get('BinName')

    try:
        if BinName:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `wms`.`_bins`( `BinName`) VALUES (%s)", [BinName])
            mysql.connection.commit()
            cur.close()       
    except:
        print("There was an error inserting bin.")
    finally: 
        return redirect(url_for("index"))
    

    

@app.route('/item_management/bin/edit/execute', methods = ['POST'])
def binEdit():
    BinID = request.form.get('BinID')
    BinName = request.form.get('BinName')

    try:
        if BinID and BinName:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE `wms`.`_bins` SET `BinName` = (%s) WHERE `BinID` = (%s)", (BinName, BinID))
            mysql.connection.commit()
            cur.close()
    except:
        print("There was an error editing bin.")
    finally:
        return redirect(url_for("index"))

    

@app.route('/item_management/bin/delete/execute', methods = ['POST'])
def binDelete():
    BinID = request.form.get('BinID')

    try:
        if BinID:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM `wms`.`_bins` WHERE `BinID` = %s", [BinID])
            mysql.connection.commit()
            cur.close()
    except:
        print("There was an error removing bin")
    finally:
        return redirect(url_for("index"))

@app.route('/item_management/inventory/create/execute', methods = ['POST'])
def inventoryCreate():

    BinID = request.form.get('BinID')
    ProductID = request.form.get('ProductID')
    QTY = request.form.get('QTY')

    if ProductID and BinID and QTY: 
        try:
            
            # Check to see if this pair is already in the system
            cur = mysql.connection.cursor()
            response = cur.execute("UPDATE `wms`.`_inventory` SET `QTY` = (%s) WHERE  (`BinID` = (%s) AND `ProductID` = (%s))", (QTY, BinID, ProductID))

            if not response:
                cur.execute("INSERT INTO `wms`.`_inventory`( `ProductID`, `BinID`, `QTY`) VALUES (%s, %s, %s)", (BinID, ProductID, QTY))
            mysql.connection.commit()
            cur.close()
        except:
            print("No such product id or bin id in database")
        finally:
            return redirect(url_for("index"))
            
        

    

@app.route('/item_management/inventory/edit/execute', methods = ['POST'])
def inventoryEdit():
    InventoryID = request.form.get('InventoryID')
    QTY = request.form.get('QTY')

    try:
        if InventoryID and QTY:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE `wms`.`_inventory` SET `QTY` = (%s) WHERE `InventoryID` = (%s)", (QTY, InventoryID))
            mysql.connection.commit() 
            cur.close()    
    except:
        print("There was an error editing inventory.")
    finally:     
        return redirect(url_for("index"))
        

    

    

@app.route('/item_management/inventory/delete/execute', methods = ['POST'])
def inventoryDelete():
    InventoryID = request.form.get('InventoryID')

    try:
        if InventoryID:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM `wms`.`_inventory` WHERE `InventoryID` = %s", [InventoryID])
            mysql.connection.commit()
            
    except:
        print("There was an issue deleting inventory")
    finally:
        cur.close()
        return redirect(url_for("index"))

    

    