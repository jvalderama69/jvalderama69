from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, DataRequired, NumberRange, Required, InputRequired, Email, ValidationError
from hospital.models import Usuarios

class RegisterForm(FlaskForm):
    def validate_ident(self, ident_to_check):
        usuario = Usuarios.query.filter_by(id=ident_to_check.data).first()
        if usuario:
            raise ValidationError('Id de usuario ya existe, verifique.')
    
    def validate_email_address(self, email_address_to_check):
        email_address = Usuarios.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('correo electrónico ya existe, verifique.')

    tipoId = SelectField(label='Tipo Id.:', validators=[DataRequired()])
    ident = IntegerField(label='Identificación:', validators=[Required(), NumberRange(min=0, max=999999999)])
    tipoUsuario = SelectField(label='Usr.:', choices=[("P","Paciente"),("D","Doctor")], validators=[DataRequired()])
    nombre = StringField(label='Nombre:', validators=[Length(min=2, max=30), DataRequired()])
    apellidos = StringField(label='Apellidos:', validators=[Length(min=2, max=50), DataRequired()])
    email_address = StringField(label='Correo electrónico:', validators=[InputRequired("Ingrese el correo electrónico."), Email("Ingrese un email válido")])
    password1 = PasswordField(label='Contraseña:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirmar contraseña:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Crear usuario')

class LoginForm(FlaskForm):
    email_address = StringField(label='Correo electrónico:', validators=[InputRequired("Ingrese el correo electrónico."), Email("Ingrese un email válido")])
    password = PasswordField(label='Contraseña:', validators=[Length(min=8), DataRequired()])
    submit = SubmitField(label='Iniciar sesión')

class AgendarForm(FlaskForm):
    fecha  = StringField(label='Fecha:', validators=[Length(min=10, max=10), DataRequired()])
    hora   = StringField(label='Hora:', validators=[Length(min=5, max=5), DataRequired()])
    doctor = SelectField("Id.Doctor:", coerce=int)
    submit = SubmitField('Agendar')

class CalificarForm(FlaskForm):
    puntaje = IntegerField(label='Su puntaje: ', validators=[Required(), NumberRange(min=1, max=5)])
    submit = SubmitField('Calificar')

class ComentarForm(FlaskForm):
    comentario = StringField(label='Comentarios:', validators=[Length(min=2, max=1024), DataRequired()])
    submit = SubmitField('Registrar')
