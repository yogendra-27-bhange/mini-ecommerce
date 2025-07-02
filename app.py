from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime
import os
from flask import g

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change_this_secret_key')

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', ''),
            database=os.environ.get('DB_NAME', 'ecommerce')
        )
    return g.db

def get_cursor():
    return get_db().cursor(dictionary=True)

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('home.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    cursor = get_cursor()
    for pid, qty in cart.items():
        cursor.execute("SELECT * FROM products WHERE id = %s", (pid,))
        product = cursor.fetchone()
        if product:
            product['quantity'] = qty
            product['subtotal'] = product['price'] * qty
            total += product['subtotal']
            items.append(product)
    cursor.close()
    return render_template('cart.html', items=items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        cart = session.get('cart', {})
        db = get_db()
        cursor = db.cursor(dictionary=True)
        for pid, qty in cart.items():
            cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (%s, %s)", (pid, qty))
        db.commit()
        cursor.close()
        session.pop('cart', None)
        return render_template('checkout.html', success=True)
    return render_template('checkout.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        desc = request.form['description']
        image = request.form['image']
        cursor.execute("INSERT INTO products (name, price, description, image) VALUES (%s, %s, %s, %s)",
                       (name, price, desc, image))
        db.commit()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('admin.html', products=products)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    db.commit()
    cursor.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=False)