from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional

class LibroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    autor = StringField('Autor')
    precio = FloatField('Precio', default=0.0)
    cantidad = IntegerField('Cantidad', default=0)
    submit = SubmitField('Guardar')