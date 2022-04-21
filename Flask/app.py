#importar codigo necesario
from flask import Flask, jsonify
from markupsafe import escape
from flask_db2 import DB2
import sys

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

#podemos tener todas las rutas que queramos
@app.route("/segunda")
def segunda_ruta():
    return "<h1>segunda ruta<h1/>"
#podemos recibir variables a traves de urls
#f string formatting
@app.route("/nombre/<el_nombre>")
def nombre(el_nombre):
    return f"hola {escape(el_nombre)}, espero que est&eacute;s bien."
#converters
@app.route("/entero/<int:valor>")
def entero(valor):
    return f"El valor que mandaste fue {escape(valor)} "

@app.route("/ruta/<path:valor>")
def ruta(valor):
    return f"El valor que mandaste fue {escape(valor)} "

#lo que vamos a regresar generalmente va ser json
#ventaja flask refresar un diccionario python y se jsonifica

diccionario ={
    "nombre" : "Garfiol",
    "edad": 30,
    "peso": 64
}

@app.route ("/json")
def json():
    return diccionario

# se puede discriminar por medio de metodos de request de HTTP
# GET,POST,PUT,DELETE

@app.route ("/metodo", methods = ['GET','POST'] )
def metodo_get_post():
    return "request hecha por get o post"

@app.route ("/metodo", methods = ['PUT','DELETE'] )
def metodo_put_delete():
    return "request hecha por put o delete"

#extension de vs code thunderclient

