from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    acquisition_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html' , items=items)


# Add
@app.route('/add', methods=['POST'])
def add_item():
    product = request.form.get('product')
    category = request.form.get('category')
    quantity = request.form.get('quantity', type=int)
    price = request.form.get('price', type=float)
    acquisition_date_str = request.form.get('date')
    status = request.form.get('status')

    if product and category and quantity is not None and price is not None and acquisition_date_str and status:
        acquisition_date = datetime.strptime(acquisition_date_str, "%Y-%m-%d").date()

        new_item = Item(
            product=product,
            category=category,
            quantity=quantity,
            price=price,
            acquisition_date=acquisition_date,
            status=status
        )

        db.session.add(new_item)
        db.session.commit()

    return redirect('/')

# Delete
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')

# Update
@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'POST':
        item.product = request.form['product']
        item.category = request.form['category']
        item.quantity = request.form.get('quantity', type=int)
        item.price = request.form.get('price', type=float)
        acquisition_date_str = request.form.get('date')
        item.acquisition_date = datetime.strptime(acquisition_date_str, "%Y-%m-%d").date()
        item.status = request.form['status']

        db.session.commit()
        return redirect('/')

    return render_template('update.html', item=item)

if __name__ == '__main__':
    app.run(debug=False)