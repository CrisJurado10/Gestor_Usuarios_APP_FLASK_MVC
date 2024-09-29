from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request

def validar_contraseña_usuario(indice, mysql):
    data = request.get_json()
    contraseña_ingresada = data.get('contraseña')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (indice,))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario and check_password_hash(usuario[3], contraseña_ingresada):  # Comparar contraseña hasheada
        return jsonify({"message": "Contraseña correcta"}), 200
    else:
        return jsonify({"error": "Contraseña incorrecta"}), 401



def verificar_contraseña(indice, mysql):
    data = request.get_json()
    contraseña_ingresada = data.get('contraseña')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (indice,))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario and check_password_hash(usuario[3], contraseña_ingresada):  # Comparar contraseña hasheada
        return jsonify({'id': usuario[0], 'usuario': usuario[1], 'correo': usuario[2], 'contraseña': usuario[3]}), 200
    return jsonify({"error": "Contraseña incorrecta"}), 401

def mostrar_datos_usuario(indice, mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (indice,))
    usuario = cursor.fetchone()
    cursor.close()

    if usuario:
        return jsonify({'id': usuario[0], 'usuario': usuario[1], 'correo': usuario[2], 'contraseña': usuario[3]}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

def crear_usuario(mysql):
    try:
        if not request.json:
            return jsonify({"error": "No se recibieron datos en formato JSON"}), 400

        nuevo_usuario_data = request.json  # Cambiar a request.json para recibir datos en formato JSON

        usuario = nuevo_usuario_data.get('usuario')
        correo = nuevo_usuario_data.get('correo')
        contraseña = nuevo_usuario_data.get('contraseña')

        if not usuario or not correo or not contraseña:
            return jsonify({"error": "Faltan campos obligatorios (usuario, correo, contraseña)"}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s OR correo = %s", (usuario, correo))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            return jsonify({"error": "El usuario o correo ya existen"}), 409

        contraseña_hasheada = generate_password_hash(contraseña)

        cursor.execute("INSERT INTO usuarios (usuario, correo, contraseña) VALUES (%s, %s, %s)", 
                       (usuario, correo, contraseña_hasheada))

        nuevo_id = cursor.lastrowid
        mysql.connection.commit()
        cursor.close()

        nuevo_usuario_data = {
            'id': nuevo_id,
            'usuario': usuario,
            'correo': correo
        }
        return jsonify(nuevo_usuario_data), 201

    except Exception as e:
        print(f"Error al crear el usuario: {str(e)}")
        return jsonify({"error": f"Error al crear el usuario: {str(e)}"}), 500

def obtener_usuarios(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()

    return jsonify([{'id': usuario[0], 'usuario': usuario[1], 'correo': usuario[2], 'contraseña': usuario[3]} for usuario in usuarios]), 200

def obtener_usuario(indice, mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (indice,))
    usuario = cursor.fetchone()
    cursor.close()
    if usuario:
        return jsonify({'id': usuario[0], 'usuario': usuario[1], 'correo': usuario[2], 'contraseña': usuario[3]}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

def actualizar_usuario(indice, mysql):
    cursor = mysql.connection.cursor()
    usuario_actualizado_data = request.get_json()

    # Hashear la nueva contraseña antes de actualizar
    contraseña_hasheada = generate_password_hash(usuario_actualizado_data['contraseña'])

    # Actualizar los datos del usuario
    cursor.execute("UPDATE usuarios SET usuario = %s, correo = %s, contraseña = %s WHERE id = %s", 
                   (usuario_actualizado_data['usuario'], usuario_actualizado_data['correo'], contraseña_hasheada, indice))
    mysql.connection.commit()
    cursor.close()
    return jsonify(usuario_actualizado_data), 200

def eliminar_usuario(indice, mysql):
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (indice,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        return jsonify({"error": "Usuario no encontrado"}), 404

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (indice,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Usuario eliminado correctamente"}), 200
