#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Veritabanı tablolarını oluştur/güncelle
# Flask-Migrate kullanılıyorsa:
# flask db upgrade
# Alternatif olarak create_all() kullanmak isterseniz bir script çalıştırabilirsiniz:
python -c "from blog import app, db; app.app_context().push(); db.create_all()"
