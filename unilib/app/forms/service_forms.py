from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional


class ServiceForm(FlaskForm):
    title = StringField('Judul Layanan', validators=[DataRequired()])
    description = TextAreaField('Deskripsi', validators=[Optional()])
    icon = StringField('Ikon (Material Symbol)', validators=[Optional()])
    link_url = StringField('URL Tujuan (opsional)', validators=[Optional()])
    sort_order = IntegerField('Urutan', default=0, validators=[Optional()])
    is_active = BooleanField('Aktif', default=True)
    submit = SubmitField('Simpan')
