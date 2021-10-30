from sqlalchemy.orm import backref
from hospital import db, login_manager
from hospital import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

class Tipos(db.Model):
    codigo = db.Column(db.String(length=2), primary_key=True)
    descripcion = db.Column(db.String(length=30), nullable=False)

class Usuarios(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    tipoId = db.Column(db.String(length=2), nullable=False)
    tipoUsuario = db.Column(db.String(length=1), nullable=False)
    nombre = db.Column(db.String(length=30), nullable=False)
    apellidos = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    clave = db.Column(db.String(length=128), nullable=False)
    citas = db.relationship('Citas', backref='citas_pendientes', lazy=True)

    def __repr__(self):
        return f'Usuarios {self.nombre}'

    @property
    def mostrar_nombre(self):
        if str(self.tipoUsuario) == "P":
            return "Paciente"
        else:
            return "Doctor"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.clave = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.clave, attempted_password)

class Citas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fecha = db.Column(db.String(length=10), nullable=False)
    hora  = db.Column(db.String(length=5), nullable=False)
    idPaciente = db.Column(db.Integer(), nullable=False)
    idDoctor = db.Column(db.Integer(), db.ForeignKey('usuarios.id'))
    calificacion = db.Column(db.Integer(), nullable=True)
    comentarios = db.Column(db.String(length=1024), nullable=True)

    def yaComentado(self):
        return len(self.comentarios) > 0

    def calificar(self, elPuntaje):
        self.calificacion = elPuntaje
        db.session.commit()

    def comentar(self, elComentario):
        self.comentarios = elComentario
        db.session.commit()

    def __repr__(self):
        return f'Citas {self.fecha}'
