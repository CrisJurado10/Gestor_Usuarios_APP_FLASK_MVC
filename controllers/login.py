from flask import render_template, request, redirect, url_for, session

def login(mysql):
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        
        # Verificar las credenciales del usuario
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
        user = cur.fetchone()
        cur.close()

        if user:
            session['usuario'] = usuario  # Almacenar el usuario en la sesión
            return redirect(url_for('pagina_principal'))  # Redirigir a la página principal
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos.")
    
    return render_template('login.html')

def logout():
    session.pop('usuario', None)  # Elimina el usuario de la sesión
    return redirect(url_for('login'))  # Redirige al formulario de login

def index():
    # Redirigir a la página principal si el usuario está autenticado
    if 'usuario' in session:
        return redirect(url_for('pagina_principal'))
    return render_template('login.html')

