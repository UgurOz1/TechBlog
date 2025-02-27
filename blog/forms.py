from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL, Optional
from blog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    confirm_password = PasswordField('Şifreyi Onayla',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı seçin.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu email adresi zaten kayıtlı. Lütfen başka bir email adresi kullanın.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')

class UpdateProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                       validators=[DataRequired(), Email()])
    bio = TextAreaField('Hakkımda')
    location = StringField('Konum')
    website = StringField('Website', validators=[Optional(), URL()])
    twitter = StringField('Twitter')
    instagram = StringField('Instagram')
    github = StringField('GitHub')
    submit = SubmitField('Güncelle')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı seçin.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Bu email adresi zaten kayıtlı. Lütfen başka bir email adresi kullanın.')

class PostForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired()])
    content = TextAreaField('İçerik', validators=[DataRequired()])
    image = FileField('Görsel', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Sadece resim dosyaları yüklenebilir!')])
    submit = SubmitField('Gönder')

class CommentForm(FlaskForm):
    content = TextAreaField('Yorum', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Gönder') 