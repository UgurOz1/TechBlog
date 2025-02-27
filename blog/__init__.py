from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_mail import Mail

# .env dosyasını yükle
load_dotenv()

# Flask uygulamasını oluştur
app = Flask(__name__)

# Uygulama yapılandırmaları
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'gelistirme-icin-gizli-anahtar')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanı bağlantısını oluştur
db = SQLAlchemy(app)

# Şifreleme için bcrypt
bcrypt = Bcrypt(app)

# Kullanıcı yönetimi için login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Lütfen giriş yapın.'
login_manager.login_message_category = 'info'

# Mail konfigürasyonu
mail = Mail()

# Blueprint'leri kaydet
from blog.auth import auth as auth_blueprint
from blog.main import main as main_blueprint
from blog.users import users as users_blueprint
from blog.admin import admin as admin_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)

# Modelleri içe aktar
from blog import models

# Veritabanını oluştur
with app.app_context():
    db.create_all()
    print("Veritabanı tabloları oluşturuldu!")

migrate = Migrate(app, db)

# Mail konfigürasyonu
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail.init_app(app) 