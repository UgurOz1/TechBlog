import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Temel Konfigürasyon
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-uret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///blog.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail Ayarları
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER')
    
    # Upload Ayarları
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    UPLOAD_FOLDER = 'static/post_images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Production SSL/HTTPS ayarları
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # Production Cache ayarları
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 yıl
    
    # Production Güvenlik Başlıkları
    STRICT_TRANSPORT_SECURITY = True
    CONTENT_SECURITY_POLICY = True

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False 