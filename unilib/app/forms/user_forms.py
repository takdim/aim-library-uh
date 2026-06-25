from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError
from app.models.user import User


class UserCreateForm(FlaskForm):
    full_name = StringField('Nama Lengkap', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password minimal 6 karakter.')
    ])
    confirm_password = PasswordField('Konfirmasi Password', validators=[
        EqualTo('password', message='Password tidak cocok.')
    ])
    role = SelectField('Role', choices=[('staff', 'Staff'), ('admin', 'Admin')])
    submit = SubmitField('Buat Akun')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email sudah digunakan.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username sudah digunakan.')


class UserEditForm(FlaskForm):
    full_name = StringField('Nama Lengkap', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    role = SelectField('Role', choices=[('staff', 'Staff'), ('admin', 'Admin')])
    is_active = BooleanField('Akun Aktif')
    new_password = PasswordField('Password Baru (kosongkan jika tidak diubah)', validators=[Optional()])
    submit = SubmitField('Simpan Perubahan')
