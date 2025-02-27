from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from slugify import slugify

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    twitter = db.Column(db.String(100), nullable=True)
    instagram = db.Column(db.String(100), nullable=True)
    github = db.Column(db.String(100), nullable=True)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    likes = db.relationship('PostLike', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_total_posts(self):
        return len(self.posts)

    def get_total_likes_received(self):
        return sum(post.like_count() for post in self.posts)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_post.jpg')
    views = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('PostLike', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    def like_count(self):
        return len(self.likes)
    
    def is_liked_by(self, user):
        return PostLike.query.filter_by(user_id=user.id, post_id=self.id).first() is not None

    def comment_count(self):
        return len(self.comments)

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date_liked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')" 