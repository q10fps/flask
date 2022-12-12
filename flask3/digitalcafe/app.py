from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session

import database as db
import authentication
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)
# Set the secret key to some random bytes. 
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

navbar = """
        <a href='/'>Home</a> | <a href='/products'>Products</a> |
        <a href='/branches'>Branches</a> | <a href='/aboutus'>About Us</a> |
        <a href='/login'>Login</a>

         """

@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
    return render_template('branches.html', page="Branches")

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

#
@app.route('/login', methods=['GET', 'POST'])


def login():
    return render_template('login.html')


@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if is_successful:
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/login?error=Invalid username or password. Please try again.')

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')


@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a 
    # quantity of 1 for now

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/update-cart', methods=["POST"])
def update_cart():
    code = request.form.getlist("code")
    qty = request.form.getlist("qty")

    for code, qty in zip(code, qty):
        if (qty !=''):
            product = db.get_product(int(code))
            item = dict()

            item["qty"] = int(qty)
            item["name"] = product(qty)
            item["subtotal"] = product["price"]*item["qty"]
            item["code"] = code

    return redirect("/cart")

@app.route('/removeitem')
def removeitem():
    code = request. args.get('code','')
    cart = session["cart"]
    cart.pop(code)
    session[" cart"] = cart
    return redirect ('cart')