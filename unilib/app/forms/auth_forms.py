from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField('Username / Email', validators=[DataRequired(message='Wajib diisi.')])
    password = PasswordField('Password', validators=[DataRequired(message='Wajib diisi.')])
    remember_me = BooleanField('Ingat Saya')
    submit = SubmitField('Masuk')
