from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del libro', validators=[DataRequired(), Length(max=100)])
    autor = StringField('Autor', validators=[Optional(), Length(max=100)])
    precio = FloatField('Precio', validators=[Optional()], default=0.0)
    cantidad = IntegerField('Cantidad', validators=[Optional()], default=0)
    submit = SubmitField('Guardar')
    
class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    mail = StringField('Correo electrónico', validators=[DataRequired(), Length(max=100)])
    password = StringField('Contraseña', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField('Guardar usuario')
    

# form.py

class LoginForm(FlaskForm):
    """Formulario para iniciar sesión"""
    email = StringField('Correo electrónico', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class RegistroForm(FlaskForm):
    """Formulario para registrar nuevo usuario"""
    nombre = StringField('Nombre completo', validators=[DataRequired(), Length(max=100)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Length(max=100), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar contraseña', 
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')