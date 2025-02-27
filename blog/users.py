from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
from blog import db
from blog.models import User, Post
from blog.forms import UpdateProfileForm

users = Blueprint('users', __name__)

@users.route("/profile/<string:username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('profile.html', user=user, posts=posts)

@users.route("/profile/edit", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        current_user.twitter = form.twitter.data
        current_user.instagram = form.instagram.data
        current_user.github = form.github.data
        
        db.session.commit()
        flash('Profiliniz başarıyla güncellendi!', 'success')
        return redirect(url_for('users.profile', username=current_user.username))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.website.data = current_user.website
        form.twitter.data = current_user.twitter
        form.instagram.data = current_user.instagram
        form.github.data = current_user.github
    
    return render_template('edit_profile.html', title='Profili Düzenle', form=form) 