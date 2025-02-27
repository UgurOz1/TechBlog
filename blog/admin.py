from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from blog import db
from blog.models import User, Post, Comment
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Bu sayfaya erişim yetkiniz yok!', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route("/admin")
@login_required
@admin_required
def admin_panel():
    users = User.query.all()
    total_users = len(users)
    total_posts = Post.query.count()
    total_comments = Comment.query.count()
    
    # Son eklenen blog yazılarını al
    recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         users=users,
                         total_users=total_users,
                         total_posts=total_posts,
                         total_comments=total_comments,
                         recent_posts=recent_posts)

@admin.route("/admin/users")
@login_required
@admin_required
def user_list():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.join_date.desc()).paginate(page=page, per_page=10)
    return render_template('admin/users.html', users=users)

@admin.route("/admin/posts")
@login_required
@admin_required
def post_list():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('admin/posts.html', posts=posts)

@admin.route("/admin/post/<int:post_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f'"{post.title}" başlıklı yazı silindi!', 'success')
    return redirect(url_for('admin.post_list'))

@admin.route("/admin/post/<int:post_id>/toggle_visibility", methods=['POST'])
@login_required
@admin_required
def toggle_post_visibility(post_id):
    post = Post.query.get_or_404(post_id)
    post.is_visible = not post.is_visible
    db.session.commit()
    status = "görünür" if post.is_visible else "gizli"
    flash(f'"{post.title}" başlıklı yazı {status} yapıldı!', 'success')
    return redirect(url_for('admin.post_list'))

@admin.route("/admin/user/<int:user_id>/toggle_admin", methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('Kendi admin durumunuzu değiştiremezsiniz!', 'danger')
    else:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f"'{user.username}' için admin durumu güncellendi!", 'success')
    return redirect(url_for('admin.user_list'))

@admin.route("/admin/user/<int:user_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('Kendi hesabınızı silemezsiniz!', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f"'{user.username}' kullanıcısı silindi!", 'success')
    return redirect(url_for('admin.user_list')) 