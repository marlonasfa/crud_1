from flask import Flask, abort, redirect, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# CONFIGURACIÓN MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_alumnos'

mysql = MySQL(app)


# MOSTRAR DATOS
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM alumnos')
    alumnos = cursor.fetchall()
    cursor.close()
    return render_template('index.html', alumnos=alumnos)


# AGREGAR
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO alumnos(nombre, correo, telefono) VALUES(%s,%s,%s)',
            (nombre, correo, telefono),
        )
        mysql.connection.commit()
        cursor.close()
        return redirect('/')

    return render_template('agregar.html')


# EDITAR
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']

        cursor.execute(
            'UPDATE alumnos SET nombre=%s, correo=%s, telefono=%s WHERE id=%s',
            (nombre, correo, telefono, id),
        )
        mysql.connection.commit()
        cursor.close()
        return redirect('/')

    cursor.execute('SELECT * FROM alumnos WHERE id=%s', [id])
    alumno = cursor.fetchone()
    cursor.close()

    if alumno is None:
        abort(404)

    return render_template('editar.html', alumno=alumno)


# ELIMINAR
@app.route('/eliminar/<int:id>')
def eliminar(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM alumnos WHERE id=%s', [id])
    mysql.connection.commit()
    cursor.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
