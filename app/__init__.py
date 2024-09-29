from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_migrate import Migrate


# Inisialisasi extension Flask
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()
migrate = Migrate()

# Memuat variable dari file .env
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Memuat konfigurasi dari config.py atau file lain
    app.config.from_object('config.Config')
    
    # Inisialisasi database dan extension lainnya
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    
    # Tentukan halaman login Flask-Login
    login_manager.login_view = 'main.login'

     # Fungsi user_loader untuk memuat user dari database berdasarkan ID
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User 
        return User.query.get(int(user_id))  # Mengambil user berdasarkan ID dari database
    
    # Import blueprint dan register
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
