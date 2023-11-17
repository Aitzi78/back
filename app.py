from flask import Flask, jsonify, request,abort,redirect
import mysql.connector
from config import AplicacionConfig
from models import db, Administrador, Preguntas, Respuestas, rangoResultado
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(AplicacionConfig)
cors = CORS(app)
db.init_app(app)





# rutas Preguntas

@app.route('/api/Preguntas', methods=['GET'])

def obtener_pregunta():
    preguntas = Preguntas.query.all() 
    preguntas_json = jsonify([pregunta.serialize() for pregunta in preguntas])
    return (preguntas_json)

        
@app.route('/api/Preguntas/<int:idPregunta>', methods=['GET'])
def obtener_pregunta_por_id(idPregunta):
    pregunta = Preguntas.get_by_id(idPregunta)
    if pregunta is None:
        abort(404)
    pregunta_json = jsonify(pregunta.serialize())    
    return pregunta_json

@app.route('/api/Preguntas', methods=['POST'])

def crear_pregunta():
    # obtenemos testo pregunta
    textoPregunta = request.json["textoPreguntas"]
    # creamos nueva pregunta
    nuevaPregunta = Preguntas(textoPreguntas = textoPregunta)
    # guardamos en la base de datos
    nuevaPregunta.save()
    nuevaPregunta_json = jsonify(nuevaPregunta.serialize())
    return nuevaPregunta_json, 201


@app.route('/api/Preguntas/<int:idPregunta>', methods=['PUT'])
def actualizar_pregunta_por_id(idPregunta):
    # obtenemos texto pregunta por id
     textoPregunta_actualizada = request.json["textoPreguntas"]
     #buscamos pregunta por id
     pregunta = Preguntas.query.get(idPregunta)
     if pregunta is None:
         abort(404)
     # actualizar texto de la pregunta
     pregunta.textoPreguntas  = textoPregunta_actualizada
     #guardamos pregunta
     pregunta.save()  
     pregunta_json = jsonify(pregunta.serialize()) 
     return pregunta_json

@app.route('/api/Preguntas/<int:idPregunta>', methods=['DELETE'])
def eliminar_pregunta_por_id(idPregunta):
    pregunta = Preguntas.get_by_id(idPregunta)
    if pregunta is None:
        abort(404)
    pregunta.delete()   
    return (""), 204

#ruta Respuestas

@app.route('/api/Respuestas/<int:idPregunta>', methods=['GET'])
def obtener_respuestas_por_id(idPregunta):
    #filtramos respuesta por id de pregunta
    respuestas = Respuestas.query.filter_by(idPreguntas= idPregunta).all()
   
    if respuestas is None:
        abort(404)
    print (respuestas)
    respuestas_json = jsonify([respuesta.serialize() for respuesta in respuestas ])    
    return respuestas_json

#rutas Administrador
@app.route("/api/out/login", methods=["POST"])
def login():
    nombreUsuario = request.json["nombreUsuario"]
    password = request.json["contraseña"]
    #verificamos si el usuario existe
    admin = Administrador.query.filter_by(nombreUsuario = nombreUsuario).first()
    if admin is None:
        return jsonify({"Error: no autorizado"},401)
    if not admin.check_contraseña(password):
        return jsonify({"Error: no autorizado"},401)
    return jsonify({"nombreUsuario": nombreUsuario,"contraseña": password})
    

    


if __name__ == '__main__':
    app.run(debug=True)
