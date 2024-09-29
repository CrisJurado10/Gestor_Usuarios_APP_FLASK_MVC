from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from controllers.usuario_controller import crear_usuario, obtener_usuarios, obtener_usuario, actualizar_usuario, eliminar_usuario

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Usuario de MYSQL
app.config['MYSQL_PASSWORD'] = 'root'  # Contraseña de MYSQL
app.config['MYSQL_DB'] = 'Crud_Usuarios'
app.secret_key = 'tu_clave_secreta'  # Cambia esto por una clave más segura

mysql = MySQL(app)



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
            return redirect(url_for('pagina_principal'))
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos.")
    
    return render_template('login.html')

@app.route('/pagina_principal')
def pagina_principal():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('index.html', usuario=session['usuario'])

@app.route('/usuarios', methods=['GET'])
def usuarios():
    return obtener_usuarios(mysql)

@app.route('/usuarios', methods=['POST'])
def crear():
    return crear_usuario(mysql)

@app.route('/usuarios/<int:indice>', methods=['GET'])
def obtener_indice(indice):
    return obtener_usuario(indice, mysql)

@app.route('/usuarios/<int:indice>', methods=['PUT'])
def actualizar(indice):
    return actualizar_usuario(indice, mysql)

@app.route('/usuarios/<int:indice>', methods=['DELETE'])
def eliminar(indice):
    return eliminar_usuario(indice, mysql)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

##Visualizar con contraseña en texto plano
@app.route('/visualizar', methods=['POST'])
def visualizar():
    data = request.get_json()
    id_usuario = data.get('id')
    contraseña_ingresada = data.get('contraseña')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()

    # Comparar la contraseña directamente sin hashearla
    if usuario and usuario[3] == contraseña_ingresada:  # Comparación directa
        return jsonify({'id': usuario[0], 'usuario': usuario[1], 'correo': usuario[2]}), 200
    else:
        return jsonify({"error": "Contraseña incorrecta"}), 401


if __name__ == '__main__':
    app.run(debug=True)
