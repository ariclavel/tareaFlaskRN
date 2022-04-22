#importar codigo necesario
from flask import Flask, jsonify
from markupsafe import escape
from flask_db2 import DB2
import sys
from flask_cors import CORS

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

