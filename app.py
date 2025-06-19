from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'orders.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT,
                product TEXT,
                quantity INTEGER,
                address TEXT,
                status TEXT DEFAULT 'Pending'
            )
        ''')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        customer = request.form['customer']
        product = request.form['product']
        quantity = request.form['quantity']
        address = request.form['address']
        with sqlite3.connect(DB) as conn:
            conn.execute("INSERT INTO orders (customer, product, quantity, address) VALUES (?, ?, ?, ?)",
                         (customer, product, quantity, address))
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/track', methods=['GET', 'POST'])
def track():
    order = None
    if request.method == 'POST':
        order_id = request.form['order_id']
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    return render_template('track.html', order=order)


@app.route('/admin')
def admin():
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        orders = conn.execute("SELECT * FROM orders").fetchall()
    return render_template('admin.html', orders=orders)

@app.route('/update/<int:oid>', methods=['GET', 'POST'])
def update(oid):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        if request.method == 'POST':
            status = request.form['status']
            conn.execute("UPDATE orders SET status=? WHERE id=?", (status, oid))
            return redirect(url_for('admin'))
        order = conn.execute("SELECT * FROM orders WHERE id=?", (oid,)).fetchone()
    return render_template('update.html', order=order)

@app.route('/delete/<int:oid>')
def delete(oid):
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM orders WHERE id=?", (oid,))
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
