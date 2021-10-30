from flask.helpers import flash
from hospital import app
from flask import render_template, redirect, url_for, flash, request
from hospital.models import Citas, Usuarios, Tipos
from hospital.forms import RegisterForm, LoginForm, AgendarForm, CalificarForm, ComentarForm
from hospital import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/inicio")
def home_page():
    return render_template('home.html')

@app.route("/citas", methods=['GET','POST'])
@login_required
def citas_page():
    calificar_form = CalificarForm()
    if request.method == "POST":
        citaId = request.form.get('idCitas')
        citaPuntaje = request.form.get('puntaje')
        citas_object = Citas.query.filter_by(id=citaId).first()
        if citas_object:
            citas_object.calificar(citaPuntaje)
            flash(f"Ha calificado la cita: ({citas_object.calificacion})", category='success')
            return redirect(url_for('home_page'))

    if request.method == "GET":
        citas = Citas.query.filter_by(idPaciente=current_user.id, calificacion=0)
        anteriores = Citas.query.all()
        return render_template('citas.html', citas=citas, anteriores=anteriores, calificar_form=calificar_form)

@app.route("/citad", methods=['GET','POST'])
@login_required
def citad_page():
    comentar_form = ComentarForm()
    if request.method == "POST":
        citaId = request.form.get('idCitas')
        citaComentario = request.form.get('comentario')
        citas_object = Citas.query.filter_by(id=citaId).first()
        if citas_object:
            citas_object.comentar(citaComentario)
            flash("Comentarios ingresados exitosamente.", category='success')
            return redirect(url_for('home_page'))

    if request.method == "GET":
        citas = Citas.query.filter_by(idDoctor=current_user.id, calificacion=0)
        anteriores = Citas.query.filter_by(idDoctor=current_user.id)
        return render_template('citad.html', citas=citas, anteriores=anteriores, comentar_form=comentar_form)

@app.route("/agendar", methods=['GET','POST'])
def agendar_page():
    form=AgendarForm()
    doctores = [(c.id, c.nombre+" "+c.apellidos) for c in Usuarios.query.filter_by(tipoUsuario="D")]
    form.doctor.choices = doctores
    if form.validate_on_submit():
        cita_nueva = Citas(fecha=form.fecha.data, hora=form.hora.data, 
                           idPaciente=current_user.id, idDoctor=form.doctor.data,
                           calificacion=0)
        db.session.add(cita_nueva)
        db.session.commit()
        flash('agendamiento realizado.', category='success')
        return redirect(url_for('home_page'))
    return render_template('agendar.html', form=form)

@app.route('/registro', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    tipos = [(c.codigo, c.descripcion) for c in Tipos.query.all()]
    form.tipoId.choices = tipos
    if form.validate_on_submit():
        usuario_nuevo = Usuarios(tipoId=form.tipoId.data, id=form.ident.data,
                                tipoUsuario=form.tipoUsuario.data, nombre=form.nombre.data,
                                apellidos=form.apellidos.data, email=form.email_address.data,
                                password=form.password1.data)
        db.session.add(usuario_nuevo)
        db.session.commit()

        login_user(usuario_nuevo)
        flash(f"Usuario creado exitosamente, Hola {usuario_nuevo.nombre}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'Error en el registro: {err_msg}', category='danger')
    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Usuarios.query.filter_by(email=form.email_address.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Se ha logueado como {attempted_user.nombre}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Email o clave inválida, intente de nuevo.', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("Su sesión ha finalizado.", category='info')
    return redirect(url_for("home_page"))