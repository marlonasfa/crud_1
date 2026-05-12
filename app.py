from flask import Flask, render_template, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumnos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELO
class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))

# CREAR BD
with app.app_context():
    db.create_all()

# LISTAR
@app.route('/')
def index():
    alumnos = Alumno.query.all()
    return render_template('index.html', alumnos=alumnos)

# AGREGAR
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nuevo = Alumno(
            nombre=request.form['nombre'],
            correo=request.form['correo'],
            telefono=request.form['telefono']
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect('/')
    return render_template('agregar.html')

# EDITAR
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    alumno = Alumno.query.get(id)
    if not alumno:
        abort(404)

    if request.method == 'POST':
        alumno.nombre = request.form['nombre']
        alumno.correo = request.form['correo']
        alumno.telefono = request.form['telefono']
        db.session.commit()
        return redirect('/')

    return render_template('editar.html', alumno=alumno)

# ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    alumno = Alumno.query.get(id)
    if alumno:
        db.session.delete(alumno)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)