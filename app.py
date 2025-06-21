from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL config
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce"
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def home():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
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
    for pid, qty in cart.items():
        cursor.execute("SELECT * FROM products WHERE id = %s", (pid,))
        product = cursor.fetchone()
        if product:
            product['quantity'] = qty
            product['subtotal'] = product['price'] * qty
            total += product['subtotal']
            items.append(product)
    return render_template('cart.html', items=items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        cart = session.get('cart', {})
        for pid, qty in cart.items():
            cursor.execute("INSERT INTO orders (product_id, quantity) VALUES (%s, %s)", (pid, qty))
        conn.commit()
        session.pop('cart', None)
        return render_template('checkout.html', success=True)
    return render_template('checkout.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        desc = request.form['description']
        image = request.form['image']
        cursor.execute("INSERT INTO products (name, price, description, image) VALUES (%s, %s, %s, %s)",
                       (name, price, desc, image))
        conn.commit()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('admin.html', products=products)

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)