from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class NewsForm(FlaskForm):
    title = StringField('Judul Berita', validators=[
        DataRequired(message='Judul wajib diisi.'),
        Length(max=255, message='Judul maksimal 255 karakter.')
    ])
    category = SelectField('Kategori', choices=[
        ('Riset', 'Riset'),
        ('Event', 'Event'),
        ('Akademik', 'Akademik'),
        ('Layanan', 'Layanan'),
        ('Umum', 'Umum'),
    ])
    excerpt = TextAreaField('Ringkasan', validators=[Optional(), Length(max=500)])
    content = TextAreaField('Isi Konten', validators=[DataRequired(message='Konten wajib diisi.')])
    cover_image = FileField('Gambar Cover', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Hanya gambar (JPG, PNG, WebP).')
    ])
    status = SelectField('Status', choices=[
        ('draft', 'Draft'),
        ('published', 'Publish'),
    ])
    submit = SubmitField('Simpan')
