from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify, current_app, send_file, make_response
from flask_login import current_user, login_required
from blog import db, mail
from blog.models import Post, PostLike, Comment
from blog.forms import PostForm, CommentForm
import os
import secrets
from PIL import Image
import pdfkit
from datetime import datetime
import io
from xml.etree import ElementTree as ET
from xml.dom import minidom
from flask_mail import Message

main = Blueprint('main', __name__)

# wkhtmltopdf konfigürasyonu
if os.name == 'nt':  # Windows
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
else:  # Linux/Render
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

def save_post_image(form_image):
    if form_image:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_image.filename)
        image_fn = random_hex + f_ext
        image_path = os.path.join(current_app.root_path, 'static/post_images', image_fn)
        
        # Resmi yeniden boyutlandır
        output_size = (800, 500)
        i = Image.open(form_image)
        i.thumbnail(output_size)
        
        # Resmi kaydet
        i.save(image_path)
        
        return image_fn
    return None

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = save_post_image(form.image.data)
        
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
            image_file=image_file if image_file else 'default_post.jpg'
        )
        db.session.add(post)
        db.session.commit()
        flash('Blog yazınız oluşturuldu!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Yeni Blog Yazısı',
                         form=form, legend='Yeni Blog Yazısı')

@main.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data,
                            post=post,
                            author=current_user)
            db.session.add(comment)
            db.session.commit()
            flash('Yorumunuz başarıyla eklendi!', 'success')
            return redirect(url_for('main.post', post_id=post.id))
        else:
            flash('Yorum yapmak için giriş yapmalısınız.', 'info')
            return redirect(url_for('auth.login'))
    
    # Görüntülenme sayısını artır
    if not current_user.is_authenticated or current_user != post.author:
        post.views += 1
        db.session.commit()
    
    return render_template('post.html', title=post.title, post=post, form=form)

@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            # Eski resmi sil (default resim değilse)
            if post.image_file != 'default_post.jpg':
                old_image_path = os.path.join(current_app.root_path, 'static/post_images', post.image_file)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Yeni resmi kaydet
            image_file = save_post_image(form.image.data)
            post.image_file = image_file
        
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Blog yazınız güncellendi!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Blog Yazısını Güncelle',
                         form=form, legend='Blog Yazısını Güncelle')

@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        
    # Resmi sil (default resim değilse)
    if post.image_file != 'default_post.jpg':
        image_path = os.path.join(current_app.root_path, 'static/post_images', post.image_file)
        if os.path.exists(image_path):
            os.remove(image_path)
            
    db.session.delete(post)
    db.session.commit()
    flash('Blog yazınız silindi!', 'success')
    return redirect(url_for('main.home'))

@main.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    like = PostLike.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if like:
        db.session.delete(like)
        db.session.commit()
        return jsonify({'status': 'unliked', 'likes': post.like_count()})
    else:
        like = PostLike(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'status': 'liked', 'likes': post.like_count()})

@main.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    flash('Yorumunuz silindi!', 'success')
    return redirect(url_for('main.post', post_id=post_id))

@main.route("/post/<int:post_id>/export/<format>")
def export_post(post_id, format):
    post = Post.query.get_or_404(post_id)
    
    if format == 'pdf':
        # PDF için HTML şablonu oluştur
        html_content = f'''
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
                    .title {{ font-size: 24px; font-weight: bold; margin-bottom: 20px; text-align: center; }}
                    .meta {{ color: #666; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
                    .content {{ font-size: 16px; }}
                    img {{ max-width: 100%; height: auto; }}
                </style>
            </head>
            <body>
                <div class="title">{post.title}</div>
                <div class="meta">
                    <strong>Yazar:</strong> {post.author.username}<br>
                    <strong>Tarih:</strong> {post.date_posted.strftime('%d %B %Y')}<br>
                    <strong>Görüntülenme:</strong> {post.views}<br>
                    <strong>Beğeni:</strong> {post.like_count()}<br>
                    <strong>Yorum:</strong> {post.comment_count()}
                </div>
                <div class="content">
                    {post.content}
                </div>
            </body>
        </html>
        '''
        
        # PDF oluştur
        try:
            options = {
                'encoding': 'UTF-8',
                'page-size': 'A4',
                'margin-top': '15mm',
                'margin-right': '15mm',
                'margin-bottom': '15mm',
                'margin-left': '15mm',
            }
            
            pdf = pdfkit.from_string(html_content, False, options=options, configuration=config)
            stream = io.BytesIO(pdf)
            
            # PDF dosyasını indir
            return send_file(
                stream,
                download_name=f"{post.title}_{datetime.now().strftime('%Y%m%d')}.pdf",
                as_attachment=True,
                mimetype='application/pdf'
            )
        except Exception as e:
            print(f"PDF oluşturma hatası: {str(e)}")  # Hata mesajını konsola yazdır
            flash('PDF oluşturulurken bir hata oluştu. Lütfen wkhtmltopdf kurulumunu kontrol edin.', 'danger')
            return redirect(url_for('main.post', post_id=post_id))
            
    flash('Desteklenmeyen format.', 'warning')
    return redirect(url_for('main.post', post_id=post_id))

@main.route("/sitemap.xml")
def sitemap():
    """Generate sitemap.xml."""
    pages = []
    ten_days_ago = datetime.now() - datetime.timedelta(days=10)
    
    # Statik sayfalar
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append([url_for(rule.endpoint, _external=True), 'weekly', '0.8'])
    
    # Blog yazıları
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    for post in posts:
        url = url_for('main.post', post_id=post.id, _external=True)
        modified_time = post.date_posted.isoformat()
        pages.append([url, 'daily' if post.date_posted > ten_days_ago else 'weekly', '0.9'])
    
    # XML oluştur
    sitemap_xml = minidom.Document()
    urlset = sitemap_xml.createElement("urlset")
    urlset.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for page in pages:
        url = sitemap_xml.createElement("url")
        loc = sitemap_xml.createElement("loc")
        loc.appendChild(sitemap_xml.createTextNode(page[0]))
        url.appendChild(loc)
        
        changefreq = sitemap_xml.createElement("changefreq")
        changefreq.appendChild(sitemap_xml.createTextNode(page[1]))
        url.appendChild(changefreq)
        
        priority = sitemap_xml.createElement("priority")
        priority.appendChild(sitemap_xml.createTextNode(page[2]))
        url.appendChild(priority)
        
        urlset.appendChild(url)
    
    sitemap_xml.appendChild(urlset)
    response = make_response(sitemap_xml.toprettyxml(indent="  "))
    response.headers["Content-Type"] = "application/xml"
    
    return response

@main.route("/iletisim", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')
            
            if not all([name, email, subject, message]):
                flash('Lütfen tüm alanları doldurun.', 'danger')
                return redirect(url_for('main.contact'))
            
            # Ana mesaj
            msg = Message(
                subject=f'TechBlog İletişim Formu: {subject}',
                recipients=[current_app.config['MAIL_USERNAME']],
                reply_to=email,
                body=f'''Gönderen: {name} <{email}>

Konu: {subject}

Mesaj:
{message}
'''
            )
            
            # Otomatik yanıt
            auto_reply = Message(
                subject='TechBlog - Mesajınız Alındı',
                recipients=[email],
                body=f'''Sayın {name},

Mesajınız başarıyla alınmıştır. En kısa sürede size dönüş yapacağız.

İlettiğiniz mesaj:
{message}

Saygılarımızla,
TechBlog Ekibi
'''
            )
            
            # E-postaları gönder
            with current_app.app_context():
                mail.send(msg)
                mail.send(auto_reply)
            
            flash('Mesajınız başarıyla gönderildi! Size e-posta ile bilgi verdik.', 'success')
            
        except Exception as e:
            current_app.logger.error(f"E-posta gönderme hatası: {str(e)}")
            flash('Mesaj gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.', 'danger')
            
        return redirect(url_for('main.contact'))
        
    return render_template('contact.html', title='İletişim') 