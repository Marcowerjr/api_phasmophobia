from flask import jsonify, request
from flask_pymongo import pymongo
from app import create_app
from bson.json_util import dumps
import db_config as db


app = create_app()


@app.route('/api/all_ghosts/', methods=['GET'])
def show_ghosts():
    all_ghosts=dumps(list(db.db.phasmophobia.find()))
    return all_ghosts    


@app.route('/api/ghost/<int:n_ghost>/', methods=['GET'])
def show_a_ghost(n_ghost):
    ghost=dumps(db.db.phasmophobia.find_one({"n_ghost":n_ghost}))
    if ghost != "null":
        return ghost
    else:
        return jsonify({
                "status":404,
                "message":"Tipo de fantasma no existente",
            })
    

@app.route('/<string:password>/api/add_ghost/', methods=['POST'])
def add_new_ghost(password):
    if password=="phasmophobia":
        if len(request.json) == 6:
            db.db.phasmophobia.insert_one({
                "n_ghost":request.json["n_ghost"],
                "tipo":request.json["tipo"],
                "description":request.json["description"],
                "puntos_fuertes":request.json["puntos_fuertes"],
                "puntos_debiles":request.json["puntos_debiles"],
                "pruebas_para_detectarlo":request.json["pruebas_para_detectarlo"],
            })
        else:
            return jsonify({
                "ERROR":"ERROR",
                "message":"Te faltan datos",
            })

        return jsonify({
            "message":f"El fantasma de tipo {request.json['tipo']} se ha añadido satisfactoriamente",
            "status":200,
        })
    else:
        return jsonify({
            "status":404,
            "message":"Contraseña errónea"
        })

@app.route('/<string:password>/api/ghost/update/<int:n_ghost>/', methods=['PUT'])
def update_ghost(n_top, password):
    if password=="phasmophobia":
        if db.db.phasmophobia.find_one({'n_ghost' : request.json["n_ghost"]}):
            db.db.phasmophobia.update_one({'n_ghost' : request.json["n_ghost"]},
            {'$set':{
                "n_ghost":request.json["n_ghost"],
                "tipo":request.json["tipo"],
                "description":request.json["description"],
                "puntos_fuertes":request.json["puntos_fuertes"],
                "puntos_debiles":request.json["puntos_debiles"],
                "pruebas_para_detectarlo":request.json["pruebas_para_detectarlo"],
            }})
        else:
            return jsonify({'status':400, "message": f"Fantasma de tipo {request.json['tipo']} no existe"})

        return jsonify({'status':200, "message": f"El fantasma de tipo {request.json['tipo']} fue actualizado"})
    else:
        return jsonify({
            "status":404,
            "message":"Contraseña errónea"
        })

@app.route('/<string:password>/api/ghost/delete/<int:n_ghost>/', methods=['DELETE'])
def delete_song(n_top, password):
    if password=="phasmophobia":
        if db.db.phasmophobia.find_one({'n_ghost' : request.json["n_ghost"]}):
            db.db.phasmophobia.delete_one({'n_ghost' : request.json["n_ghost"]})
        else:
            return jsonify({'status':400, "message": f"Fantasma de tipo {request.json['tipo']} no existe"})

        return jsonify({"status":200, "message": f"El fantasma de tipo {request.json['tipo']} fue eliminado"})
    else:
        return jsonify({
            "status":404,
            "message":"Contraseña errónea"
        })


if __name__ == "__main__":
    app.run(load_dotenv=True, port=8080)

