from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional


class ProfileSectionForm(FlaskForm):
    title = StringField('Judul Section', validators=[DataRequired()])
    title_en = StringField('Title (English)', validators=[Optional()])
    content = TextAreaField('Konten', validators=[Optional()])
    content_en = TextAreaField('Content (English)', validators=[Optional()])
    image = FileField('Gambar Pendukung', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Hanya gambar.')
    ])
    submit = SubmitField('Simpan')
