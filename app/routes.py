from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db,socketio
from app.models import Product, User
from app.forms import LoginForm, CreateUserForm, AddProductForm
from flask import Blueprint
from flask_socketio import emit

main = Blueprint('main', __name__)

@socketio.on('connect')
def handle_connect():
    """Handler for new WebSocket connections."""
    emit('connect_response', {'message': 'Connected to WebSocket!'})

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid login. Please check your credentials.')
        return redirect(url_for('main.login'))
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        dob = form.dob.data
        hobby = form.hobby.data
        password = form.password.data
        user = User(name=name, email=email, dob=dob, hobby=hobby)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('main.login'))
    return render_template('create_user.html', form=form)

# Fungsi untuk menambahkan produk dan mengirim pembaruan real-time
@main.route('/add_product', methods=['GET', 'POST'])
def add_product():
    """Menambah produk ke database."""
    form = AddProductForm()
    if form.validate_on_submit():
        # Membuat produk baru dari form input
        new_product = Product(name=form.name.data, stock=form.stock.data)
        db.session.add(new_product)
        db.session.commit()

        # Emit produk terbaru ke semua client melalui WebSocket
        socketio.emit('new_product', {
            'name': new_product.name,
            'stock': new_product.stock
        },namespace='/')

        flash('Product successfully added!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_product.html', form=form)

# Route untuk menampilkan semua produk di dashboard secara real-time
@main.route('/dashboard', methods=['GET'])
def dashboard():
    """Halaman dashboard untuk menampilkan produk secara real-time."""
    products = Product.query.all()  # Mengambil semua produk dari database
    return render_template('dashboard.html', products=products)