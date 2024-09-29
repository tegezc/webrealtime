from flask_socketio import SocketIO, emit
from .models import Product, db

socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    emit('product_update', {'data': get_all_products()})

@socketio.on('new_product')
def handle_new_product(data):
    new_product = Product(name=data['name'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    emit('product_update', {'data': get_all_products()}, broadcast=True)

def get_all_products():
    products = Product.query.all()
    return [{'name': product.name, 'stock': product.stock} for product in products]
