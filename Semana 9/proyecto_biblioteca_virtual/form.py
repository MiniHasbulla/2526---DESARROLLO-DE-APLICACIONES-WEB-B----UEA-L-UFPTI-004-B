from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del libro', validators=[DataRequired(), Length(max=100)])
    autor = StringField('Autor', validators=[Optional(), Length(max=100)])
    precio = FloatField('Precio', validators=[Optional()], default=0.0)
    cantidad = IntegerField('Cantidad', validators=[Optional()], default=0)
    submit = SubmitField('Guardar')