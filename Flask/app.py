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

engine = sqlalchemy.create_engine("ibm_db_sa://db2inst1:hola@localhost:50000/testdb")
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# CÓDIGO PARA LOGIN 
# necesitamos una llave secreta 
app.secret_key = secrets.token_urlsafe(16)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)



usuarios = {"a@a.com" : {"pass" : "hola"}}

# definir una clase para contener la descripción de nuestros usuarios
class Usuario(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    
    if email not in usuarios:
        return
    
    usuario = Usuario()
    usuario.id = email
    return usuario
# método que se invoca para obtención de usuarios cuando se hace request
@login_manager.request_loader
def request_loader(request):
   
    # obtener información que nos mandan en encabezado
    key = request.headers.get('Authorization')
    print(key, file=sys.stdout)

    if key == ":":
        return None

    processed = key.split(":")

    if processed[0] in usuarios and processed[1] == usuarios[processed[0]]['pass']:
        user = Usuario()
        user.id = processed[0]
        return user

    return None
@app.route('/login', methods=['GET', 'POST'])
def login():
    # podemos verificar con qué método se accedió 
    if flask.request.method == 'GET':
        return 
    # de otra manera tuvo que ser POST
    # obtener datos 
    email = flask.request.form['email']
    # verificar validez de usuario vs fuente de datos
    if email in usuarios and flask.request.form['password'] == usuarios[email]['pass']:
        user = Usuario()
        user.id = email
        flask_login.login_user(user)
        # esta es la parte en donde pueden generar un token
        # return flask.redirect(flask.url_for('protegido'))
        return "USUARIO VALIDO",200

    # si no jaló mostrar error
    return "CREDENCIALES INVÁLIDAS",401

@app.route('/protegido')
@cross_origin()
def protegido():
    return jsonify(protegido=flask_login.current_user.is_authenticated)

@login_manager.unauthorized_handler
def handler():
    return 'No autorizado', 401

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'saliste'
    

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

@app.route("/users")
def servicio():
     # lo primero es obtener cursor 
    cur = db.connection.cursor()

     # con cursor hecho podemos ejecutar queries
    cur.execute("SELECT * FROM users")

    # obtenemos datos
    data = cur.fetchall()

    # acuerdate de cerrar el cursor
    cur.close()

    print(data, file=sys.stdout)
    resultado = []
    for current in data:
        actual = {
            "id" : current[0],
            "email" : current[1],
            "password" : current[2],
            "token": current[3],
            "fechaexp": current[4]
        }
        resultado.append(actual)

     # puedes checar alternativas para mapeo de datos
    # por hoy vamos a armar un objeto jsoneable para regresar 
    

    return jsonify(data)

