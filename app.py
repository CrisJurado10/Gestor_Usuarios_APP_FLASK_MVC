from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime

from controllers.usuario_controller import (
    crear_usuario, 
    obtener_usuarios, 
    obtener_usuario, 
    actualizar_usuario, 
    eliminar_usuario
)
app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Usuario de MYSQL
app.config['MYSQL_PASSWORD'] = 'root'  # Contraseña de MYSQL
app.config['MYSQL_DB'] = 'Crud_Usuarios'
app.secret_key = 'tu_clave_secreta'  

mysql = MySQL(app)

# Configuración de la duración de la sesión
# Configuración de la duración de la sesión 
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=15)


# Decorador para verificar si el usuario está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('pagina_principal'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], contraseña):
            session['usuario'] = usuario
            session.permanent = False  # La sesión no es permanente
            return redirect(url_for('pagina_principal'))
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos.")
    
    return render_template('login.html')

@app.route('/pagina_principal')
@login_required
def pagina_principal():
    return render_template('index.html', usuario=session['usuario'])

@app.route('/usuarios', methods=['GET'])
@login_required
def usuarios():
    return obtener_usuarios(mysql)

@app.route('/usuarios', methods=['POST'])
@login_required
def crear():
    return crear_usuario(mysql)

@app.route('/usuarios/<int:indice>', methods=['GET'])
@login_required
def obtener_indice(indice):
    return obtener_usuario(indice, mysql)

@app.route('/usuarios/<int:indice>', methods=['PUT'])
@login_required
def actualizar(indice):
    return actualizar_usuario(indice, mysql)

@app.route('/usuarios/<int:indice>', methods=['DELETE'])
@login_required
def eliminar(indice):
    return eliminar_usuario(indice, mysql)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
