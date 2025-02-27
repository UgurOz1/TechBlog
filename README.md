# Flask Blog Uygulaması

Bu proje, Flask framework'ü kullanılarak geliştirilmiş basit bir blog uygulamasıdır.

## Özellikler

- Kullanıcı kayıt ve giriş sistemi
- Blog yazısı oluşturma, düzenleme ve silme
- Ana sayfa ve detay sayfası görünümleri
- Güvenli şifre saklama

## Kurulum

1. Sanal ortam oluşturun ve aktif edin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac için
venv\Scripts\activate     # Windows için
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Veritabanını oluşturun:
```bash
flask db init
flask db migrate
flask db upgrade
```

4. Uygulamayı çalıştırın:
```bash
flask run
```

## Kullanım

- http://localhost:5000 adresinden uygulamaya erişebilirsiniz
- Kayıt olmak için "Kayıt Ol" sayfasını kullanın
- Giriş yaptıktan sonra blog yazıları oluşturabilir, düzenleyebilir ve silebilirsiniz

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 