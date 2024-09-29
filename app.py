from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from controllers.usuario_controller import crear_usuario, obtener_usuarios, obtener_usuario, actualizar_usuario, eliminar_usuario

app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)
