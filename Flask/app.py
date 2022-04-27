#importar codigo necesario
from flask import Flask, jsonify
from markupsafe import escape
from flask_db2 import DB2
import sys 
from flask_cors import CORS, cross_origin
import sqlalchemy 
from sqlalchemy import * 
import ibm_db_sa
import flask_login
import secrets 
import flask

#creamos un objeto de tipo flask
app= Flask (__name__)

#aplicar configuracion db2
app.config['DB2_DATABASE'] = 'testdb'
app.config['DB2_HOSTNAME'] = 'localhost'
app.config['DB2_PORT'] = 50000
app.config['DB2_PROTOCOL'] = 'TCPIP'
app.config['DB2_USER'] = 'db2inst1'
app.config['DB2_PASSWORD'] = 'hola'

db = DB2(app)

CORS(app)

# CÓDIGO PARA LOGIN 
# necesitamos una llave secreta 
app.secret_key = secrets.token_urlsafe(16)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# PSEUDO BASE DE DATOS DE USUARIOS
usuarios = {"a@a.com" : {"pass" : "hola"}}

# definir una clase para contener la descripción de nuestros usuarios
class Usuario(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    # verificar vs fuente de datos 
    if email not in usuarios:
        return
    
    usuario = Usuario()
    usuario.id = email
    return usuario
# método que se invoca para obtención de usuarios cuando se hace request
@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in usuarios:
        return
    
    usuario = Usuario()
    usuario.id = email
    return usuario
@app.route('/login', methods=['GET', 'POST'])
def login():
    # podemos verificar con qué método se accedió 
    if flask.request.method == 'GET':
        return '''
                <form action='login' method='POST'>
                    <input type='text' name='email' /><br />
                    <input type='password' name='password' /><br />
                    <input type='submit' name='HACER LOGIN' />
                </form>
        
        '''
    # de otra manera tuvo que ser POST
    # obtener datos 
    email = flask.request.form['email']
    # verificar validez de usuario vs fuente de datos
    if email in usuarios and flask.request.form['password'] == usuarios[email]['pass']:
        user = Usuario()
        user.id = email
        flask_login.login_user(user)
        # OJO AQUI
        # esta es la parte en donde pueden generar un token
        # return flask.redirect(flask.url_for('protegido'))
        return "USUARIO VALIDO"

    # si no jaló mostrar error
    return "CREDENCIALES INVÁLIDAS"
    

#le agregamos rutas
#@ en python significa que vamos a usar un decorator
@app.route("/")
def servicio_default():
     # lo primero es obtener cursor 
    cur = db.connection.cursor()

     # con cursor hecho podemos ejecutar queries
    cur.execute("SELECT * FROM gatitos")

    # obtenemos datos
    data = cur.fetchall()

    # acuerdate de cerrar el cursor
    cur.close()

    print(data, file=sys.stdout)

     # puedes checar alternativas para mapeo de datos
    # por hoy vamos a armar un objeto jsoneable para regresar 
    resultado = []
    for current in data:
        actual = {
            "id" : current[0],
            "nombre" : current[1],
            "peso" : current[2]
        }
        resultado.append(actual)

    return jsonify(resultado)

