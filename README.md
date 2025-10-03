# 📝 Flask Blog Uygulaması

Modern ve kullanıcı dostu bir blog platformu. Flask framework'ü kullanılarak geliştirilmiş, tam özellikli bir blog uygulamasıdır.

## 🚀 Özellikler

### 👤 Kullanıcı Yönetimi
- **Kayıt ve Giriş Sistemi**: Güvenli kullanıcı kaydı ve oturum yönetimi
- **Profil Yönetimi**: Kullanıcılar profillerini düzenleyebilir
- **Sosyal Medya Entegrasyonu**: Twitter, Instagram, GitHub bağlantıları
- **Admin Paneli**: Yönetici kullanıcılar için özel yönetim paneli

### 📖 Blog Özellikleri
- **Yazı Oluşturma**: Zengin metin editörü ile blog yazısı oluşturma
- **Görsel Yükleme**: Blog yazılarına resim ekleme
- **Yazı Düzenleme**: Mevcut yazıları düzenleme ve güncelleme
- **Yazı Silme**: İstenmeyen yazıları silme
- **Görüntülenme Sayısı**: Her yazının kaç kez görüntülendiğini takip etme

### 💬 Etkileşim Özellikleri
- **Yorum Sistemi**: Yazılara yorum yapabilme
- **Beğeni Sistemi**: Yazıları beğenebilme
- **Yanıt Sistemi**: Yorumlara yanıt verebilme
- **İstatistikler**: Kullanıcı ve yazı istatistikleri

### 🔒 Güvenlik
- **Şifre Şifreleme**: Bcrypt ile güvenli şifre saklama
- **CSRF Koruması**: Form güvenliği
- **Oturum Yönetimi**: Flask-Login ile güvenli oturum yönetimi
- **Dosya Güvenliği**: Güvenli dosya yükleme

## 🛠️ Teknolojiler

### Backend
- **Flask 3.0.2**: Web framework
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **Flask-Login**: Kullanıcı oturum yönetimi
- **Flask-Bcrypt**: Şifre şifreleme
- **Flask-WTF**: Form işleme ve CSRF koruması
- **Flask-Migrate**: Veritabanı migrasyonları
- **Flask-Mail**: E-posta gönderimi

### Frontend
- **HTML5 & CSS3**: Modern web standartları
- **Bootstrap**: Responsive tasarım
- **JavaScript**: Dinamik etkileşimler

### Veritabanı
- **SQLite**: Geliştirme ortamı için
- **PostgreSQL**: Üretim ortamı desteği

## 📁 Proje Yapısı

```
flask-blog/
├── blog/                      # Ana uygulama paketi
│   ├── __init__.py           # Uygulama fabrikası
│   ├── models.py             # Veritabanı modelleri
│   ├── forms.py              # WTForms formları
│   ├── auth.py               # Kimlik doğrulama blueprint'i
│   ├── main.py               # Ana sayfa blueprint'i
│   ├── users.py              # Kullanıcı blueprint'i
│   ├── admin.py              # Admin blueprint'i
│   ├── static/               # Statik dosyalar
│   │   ├── css/             # CSS dosyaları
│   │   ├── post_images/     # Blog yazısı görselleri
│   │   └── profile_pics/    # Profil fotoğrafları
│   └── templates/            # HTML şablonları
│       ├── layout.html      # Ana şablon
│       ├── home.html        # Ana sayfa
│       ├── post.html        # Yazı detay sayfası
│       ├── login.html       # Giriş sayfası
│       ├── register.html    # Kayıt sayfası
│       └── admin/           # Admin şablonları
├── migrations/               # Veritabanı migrasyonları
├── instance/                 # Uygulama örneği dosyaları
├── .env                      # Ortam değişkenleri
├── requirements.txt          # Python bağımlılıkları
└── run.py                   # Uygulama giriş noktası
```

## 🔧 Kurulum

### Ön Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- Git

### Adım Adım Kurulum

1. **Projeyi klonlayın:**
```bash
git clone <repository-url>
cd flask-blog
```

2. **Sanal ortam oluşturun:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Ortam değişkenlerini ayarlayın:**
`.env` dosyasını düzenleyin:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///blog.db
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=secure-password
```

5. **Veritabanını başlatın:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Uygulamayı çalıştırın:**
```bash
python run.py
```

Uygulama http://localhost:5000 adresinde çalışacaktır.

## 📊 Veritabanı Modelleri

### User (Kullanıcı)
- `id`: Benzersiz kullanıcı kimliği
- `username`: Kullanıcı adı (benzersiz)
- `email`: E-posta adresi (benzersiz)
- `password`: Şifrelenmiş şifre
- `is_admin`: Admin yetkisi
- `bio`: Kullanıcı biyografisi
- `location`: Konum bilgisi
- `website`: Web sitesi
- `social_links`: Sosyal medya bağlantıları
- `join_date`: Kayıt tarihi

### Post (Blog Yazısı)
- `id`: Benzersiz yazı kimliği
- `title`: Yazı başlığı
- `content`: Yazı içeriği
- `date_posted`: Yayınlanma tarihi
- `image_file`: Yazı görseli
- `views`: Görüntülenme sayısı
- `user_id`: Yazar kimliği

### Comment (Yorum)
- `id`: Benzersiz yorum kimliği
- `content`: Yorum içeriği
- `date_posted`: Yorum tarihi
- `user_id`: Yorum yapan kullanıcı
- `post_id`: Yorumun yapıldığı yazı
- `parent_id`: Üst yorum (yanıtlar için)

### PostLike (Beğeni)
- `id`: Benzersiz beğeni kimliği
- `user_id`: Beğenen kullanıcı
- `post_id`: Beğenilen yazı
- `date_liked`: Beğenme tarihi

## 🎯 Kullanım

### Kullanıcı İşlemleri
1. **Kayıt Olma**: Ana sayfadan "Kayıt Ol" linkine tıklayın
2. **Giriş Yapma**: E-posta ve şifrenizle giriş yapın
3. **Profil Düzenleme**: Profil sayfasından bilgilerinizi güncelleyin

### Blog İşlemleri
1. **Yazı Oluşturma**: Giriş yaptıktan sonra "Yeni Yazı" butonuna tıklayın
2. **Yazı Düzenleme**: Kendi yazılarınızın detay sayfasında "Düzenle" butonunu kullanın
3. **Yorum Yapma**: Yazı detay sayfasında yorum formunu kullanın
4. **Beğenme**: Yazı detay sayfasında kalp ikonuna tıklayın

### Admin İşlemleri
Admin kullanıcıları ek yetkilerle:
- Tüm yazıları yönetebilir
- Kullanıcıları yönetebilir
- Site istatistiklerini görüntüleyebilir

## 🔐 Güvenlik Özellikleri

- **CSRF Koruması**: Tüm formlar CSRF token ile korunur
- **Şifre Güvenliği**: Bcrypt ile hash'lenen şifreler
- **Dosya Güvenliği**: Sadece izin verilen dosya türleri yüklenebilir
- **SQL Injection Koruması**: SQLAlchemy ORM kullanımı
- **XSS Koruması**: Jinja2 template engine otomatik escape

## 🚀 Deployment

### Vercel Deployment
Proje Vercel için hazırlanmıştır:

1. Vercel hesabınıza giriş yapın
2. Projeyi GitHub'a yükleyin
3. Vercel'de "New Project" ile projeyi import edin
4. Ortam değişkenlerini Vercel dashboard'unda ayarlayın

### Geleneksel Hosting
1. Üretim ortamı için PostgreSQL veritabanı ayarlayın
2. `DATABASE_URL` ortam değişkenini güncelleyin
3. WSGI server (Gunicorn) ile deploy edin

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 İletişim

- **Geliştirici**: [Uğur Özkan]
- **E-posta**: uguro9319@gmail.com
- **GitHub**: [GitHub Profili]

## 🙏 Teşekkürler

- Flask topluluğuna
- Bootstrap ekibine
- Tüm açık kaynak katkıcılarına

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 