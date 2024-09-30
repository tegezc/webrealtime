import os
from dotenv import load_dotenv

# Memuat variabel dari file .env jika ada
load_dotenv()

class Config:
    # Secret Key untuk keamanan aplikasi (disarankan untuk menggunakan variabel environment)
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Database URI (gunakan SQLite dalam pengembangan)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Menghindari warning dari SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Konfigurasi untuk mengamankan session dan CSRF
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_PROTECTION = 'strong'

    # SocketIO Options (misalnya untuk setup di production)
    SOCKETIO_MESSAGE_QUEUE = os.getenv('SOCKETIO_MESSAGE_QUEUE') or None
    SOCKETIO_LOGGER = True
    SOCKETIO_ENGINEIO_LOGGER = True

    # Email config (jika ada keperluan untuk email notifications)
    MAIL_SERVER = os.getenv('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.getenv('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for tests
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False


