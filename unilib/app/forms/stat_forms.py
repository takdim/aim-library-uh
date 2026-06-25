from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange


class StatisticForm(FlaskForm):
    label = StringField('Label', validators=[DataRequired()])
    value = IntegerField('Nilai', validators=[DataRequired(), NumberRange(min=0)])
    icon = StringField('Ikon (Material Symbol)', validators=[Optional()])
    sort_order = IntegerField('Urutan', default=0, validators=[Optional()])
    submit = SubmitField('Simpan')
