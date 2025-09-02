"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorites_planets, Favorites_characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#[GET] /users  Listar todos los usuarios del blog. - TRAER INFO DE TODOS LOS USUARIOS 

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    print(users[0].serialize()) # los elementos de la lista se deben convertir en diccionario para poder jsonify
    users_serialized = []

    for user in users:
        users_serialized.append(user.serialize())

    return jsonify({'msg': 'OK', 'user': users_serialized}), 200


#[GET] /users  Listar un usuario del blog por ID. - TRAER INFO DE UN USUARIO 

@app.route('/user/<int:id>', methods=['GET'])
def get_single_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': f'El usuario con id {id} no existe'}), 404
    
    return jsonify({'msg': 'ok', 'user': user.serialize()}), 200


#[POST] /user - Crear un nuevo usuario
@app.route('/user', methods = ['POST'])
def create_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': ' Debes enviar info en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': f'el campo NAME es obligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': f'el campo PASSWORD es obligatorio'}), 400
    if 'email' not in body:
        return jsonify({'msg': f'el campo EMAIL es obligatorio'}), 400
    
    new_user = User()
    new_user.name = body['name']
    new_user.password = body['password']
    new_user.email = body['email']
    new_user.is_active = True
    new_user.date_suscription = "Hoy"
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'OK', 'user': new_user.serialize()})


# [GET] /people Listar todos los registros de people en la base de datos.
@app.route('/characters', methods = ['GET'])
def get_all_characters():
    characters = Characters.query.all()

    characters_serialize = []
    for character in characters:
        characters_serialize.append(character.serialize())

    return jsonify({'msg':'OK', 'character': characters_serialize})


# [GET] /people/<int:people_id> Muestra la información de un solo personaje según su id.
@app.route('/characters/<int:id>', methods = ['GET'])
def get_single_character(id):
    character = Characters.query.get(id)
    if character is None:
        return jsonify({'msg': 'No existe un personaje para es ID'})
    return jsonify({'msg': 'OK', 'character': character.serialize() })


# [GET] /planets Listar todos los registros de planets en la base de datos.
@app.route('/planets', methods = ['GET'])
def get_all_planets():
    planets = Planets.query.all()

    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())
    return jsonify({'msg': 'OK', 'planet': planets_serialized})

# [GET] /planets/<int:planet_id>
@app.route('/planets/<int:id>', methods = ['GET'])
def get_single_planet(id):
    planet = Planets.query.get(id)
    if planet is None:
        return jsonify({'msg':'No existe un planeta con el Id indicado'}), 400
    return jsonify({'msg':'OK', 'planet': planet.serialize()})


# [GET] /users/<int:user_id>/favorites Listar people y planets favoritos de un usuario
@app.route('/users/<int:id_user>/favorites', methods = ['GET'])
def get_user_favorites(id_user):
    user = User.query.get(id_user)
    if user is None:
        return jsonify({'msg': 'El ID proporcionado no esta asociado a ningun usuario'}), 404
    print(user.the_favorites_planets)
    print(user.the_favorites_characters)

    planets_favorites_serialized = []
    for favorites_planets in user.the_favorites_planets:
        planets_favorites_serialized.append(favorites_planets.planet.serialize())
    
    characters_favorites_serialized = []
    for favorites_characters in user.the_favorites_characters:
        characters_favorites_serialized.append(favorites_characters.character.serialize())
    
    return jsonify({'msg': 'OK', 'favorite_characters': characters_favorites_serialized, 'favorite_planets': planets_favorites_serialized})
    

# [POST] /favorite/<int:user_id>/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.
@app.route('/favorite/<int:id_user>/planet/<int:id_planet>', methods = ['POST'])
def create_favorite_planet(id_user, id_planet):
    new_favorite_planet = Favorites_planets()
    new_favorite_planet.id_user = id_user
    new_favorite_planet.id_planet = id_planet
    db.session.add(new_favorite_planet)
    db.session.commit()
    return jsonify({'msg': 'ok', 'favorite': new_favorite_planet.serialize()})


# [POST] /favorite/<int:user_id>/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.
@app.route('/favorite/<int:id_user>/character/<int:id_character>', methods = ['POST'])
def create_favorite_character(id_user, id_character):
    new_favorite_character = Favorites_characters()
    new_favorite_character.id_user = id_user
    new_favorite_character.id_character = id_character
    db.session.add(new_favorite_character)
    db.session.commit()
    return jsonify({'msg': 'OK', 'Character': new_favorite_character.serialize()})

# [DELETE] /favorite/<int:user_id>/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.
@app.route('/favorite/<int:id_user>/planet/<int:id_planet>', methods = ['DELETE'])
def delete_favorite_planet(id_user, id_planet):
    all_favorite_planets = Favorites_planets.query.all()
    #print(type(all_favorite_planets[0].serialize()))
    the_favorite_planets = []
    for item in all_favorite_planets:
        the_favorite_planets.append(item.serialize())
        
    for item in the_favorite_planets:
        
        if item['id_user'] == id_user and item['id_planet'] == id_planet:
            planet_to_delete = Favorites_planets.query.get(item['id'])
            db.session.delete(planet_to_delete)
            db.session.commit()
        
    return jsonify({'msg': 'Planeta Favorito borrado'})


# [DELETE] /favorite/<int:user_id>/people/<int:people_id> Elimina un people favorito con el id = people_id.
@app.route('/favorite/<int:id_user>/character/<int:id_character>', methods = ['DELETE'])
def delete_favorite_character(id_user, id_character):
    all_favorite_characters = Favorites_characters.query.all()
    the_favorite_character = []
    for item in all_favorite_characters:
        the_favorite_character.append(item.serialize())
    print(the_favorite_character)

    for item in the_favorite_character:
        
        if item['id_user'] == id_user and item['id_character'] == id_character:
            character_to_delete = Favorites_characters.query.get(item['id'])
            db.session.delete(character_to_delete)
            db.session.commit()
        
    return jsonify({'msg': 'Personaje favorito borrado'})

# [POST] crear planetas

@app.route('/planet', methods=['POST'])
def create_planet():
    body = request.get_json(silent=True)
    
    if body is None:
        return jsonify({'msg': 'Debe enviar informacion del planeta en el body'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'debes enviar un NAME para el planeta'}), 400
    if 'population' not in body:
        return jsonify({'msg': 'debes enviar la POPULATION el planeta'}), 400
    if 'climate' not in body:
        return jsonify({'msg': 'Debes enviar el CLIMATE del planeta'}), 400
    if 'gravity' not in body:
        return jsonify({'msg': 'Debes enviar el GRAVITY del planeta'}), 400
    if 'diameter' not in body:
        return jsonify({'msg': 'Debes enviar el DIAMETER del planeta'}), 400
    
    new_planet = Planets()
    new_planet.name = body['name']
    new_planet.population = body['population']
    new_planet.climate = body['climate']
    new_planet.gravity = body['gravity']
    new_planet.diameter = body['diameter']
    
    db.session.add(new_planet)
    db.session.commit()
    
    return jsonify({'msg': 'OK', 'planet': new_planet.serialize()}), 200

#[POST] CREAR CHARACTERS
@app.route('/character', methods = ['POST'])
def create_character():
    body = request.get_json(silent = True)
    if body is None:
        return jsonify({'msg': 'debes enviar la informacion del personaje'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'debes enviar un name para el personaje'}), 400
    if 'height' not in body:
        return jsonify({'msg': 'Debes enviar el height del personaje'}), 400
    if 'gender' not in body:
        return jsonify({'msg': 'debes enviar el gender del personaje'})
    if 'skin' not in body:
        return jsonify({'msg': 'debes enviar el skin del personaje'})
    if 'birth_year' not in body:
        return jsonify({'msg': ' debes enviar el birth year del personaje'})
    
    new_character = Characters()
    new_character.name = body['name']
    new_character.height = body['height']
    new_character.gender = body['gender']
    new_character.skin = body['skin']
    new_character.birth_year = body['birth_year']

    db.session.add(new_character)
    db.session.commit()

    return jsonify({'msg': 'OK', 'character': new_character.serialize()})

#[PUT] MODIFICAR REGISTRO DE PLANETAS
@app.route('/planet/<int:id_planet>', methods=['PUT'])
def update_planet(id_planet):
    planet_to_update = Planets.query.get(id_planet)
    
    if planet_to_update is None:
        return jsonify({'msg': 'El id del planeta no fue encontrado'}), 404
    
    body = request.get_json()
    if 'name' in body:
        planet_to_update.name = body['name']
    if 'population' in body:
        planet_to_update.population = body['population']
    if 'climate' in body:
        planet_to_update.climate = body['climate']
    if 'gravity' in body:
        planet_to_update.gravity = body['gravity']
    if 'diameter' in body:
        planet_to_update.diameter = body['diameter']
     
    db.session.commit()

    return jsonify({'msg': 'ok', 'planet': planet_to_update.serialize()})

#[PUT] Modificar informacion de Personajes (characters)

  


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)