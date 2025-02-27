from blog import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Veritabanı tabloları oluşturuldu!")
    app.run()
else:
    # Vercel için WSGI uygulamasını dışa aktarıyoruz
    application = app 