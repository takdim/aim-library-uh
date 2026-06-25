from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, URL, Optional, NumberRange


class NavLinkForm(FlaskForm):
    type = SelectField('Tipe', choices=[
        ('repository', 'Repository'),
        ('ejournal', 'E-Journal'),
    ])
    name = StringField('Nama Tampilan', validators=[DataRequired(), ])
    url = StringField('URL Tujuan', validators=[DataRequired()])
    description = TextAreaField('Deskripsi (untuk E-Journal)', validators=[Optional()])
    logo = FileField('Logo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Hanya gambar.')
    ])
    sort_order = IntegerField('Urutan', default=0, validators=[Optional()])
    is_active = BooleanField('Aktif', default=True)
    submit = SubmitField('Simpan')
