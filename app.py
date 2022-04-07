#from crypt import methods
import json
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

conexion = MySQL(app)

@app.route('/clientes', methods=['GET'])
def listar():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT id, nombre, apellido, edad FROM clientes"
        cursor.execute(sql)
        inf=cursor.fetchall()
        clientes=[]
        for fila in inf:
            cliente = {'id':fila[0], 'nombre':fila[1], 'apellido':fila[2], 'edad':fila[3]}
            clientes.append(cliente)

        return jsonify({'clientes':clientes, 'mensaje':"Clientes listados"})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})


@app.route('/clientes/<id>', methods=['GET'])
def leer(id):
    try: 
        cursor=conexion.connection.cursor()
        sql="SELECT id, nombre, apellido, edad FROM clientes WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        inf=cursor.fetchone()
        if inf!=None:
            cliente = {'id':inf[0], 'nombre':inf[1], 'apellido':inf[2], 'edad':inf[3]}
            return jsonify({'cliente':cliente,'mensaje':"Cliente encontrado"})
        else:
            return jsonify({'mensaje':"Cliente no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})


@app.route('/clientes', methods=['POST'])
def registrar():
    try:
        cursor = conexion.connection.cursor()
        sql="""INSERT INTO clientes (id, nombre, apellido, edad) VALUES ('{0}','{1}','{2}',
        '{3}')""".format(request.json['id'], request.json['nombre'], request.json['apellido'],
        request.json['edad'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Cliente registrado"})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})


@app.route('/clientes/<id>', methods=['PUT'])
def actualizar(id):
    try:
        cursor = conexion.connection.cursor()
        sql="UPDATE clientes SET nombre = '{0}', apellido = '{1}', edad = '{2}' WHERE id = '{3}'".format(request.json['nombre'],
        request.json['apellido'], request.json['edad'], id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Cliente actualizado"})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})


@app.route('/clientes/<id>', methods=['DELETE'])
def eliminar(id):
    try:
        cursor = conexion.connection.cursor()
        sql="DELETE FROM clientes WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje':"Cliente eliminado"})
    
    except Exception as ex:
        return jsonify({'mensaje':"Error"})


def no_encontrada(error):
    return "<h1>La pagina no existe</h1>",404

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,no_encontrada)
    app.run()
