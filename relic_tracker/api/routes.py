from flask import Blueprint, jsonify, request
from relic_tracker.helpers import token_required
from relic_tracker.models import db, User, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return jsonify({'some': 'value',
            'other' : 88.989})

# Create Character Route
@api.route('/characters', methods=['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    race = request.json['race']
    gender = request.json['gender']
    user_token = current_user_token.token

    character = Character(name, race, gender, user_token)

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# Retrieve ALL Characters
@api.route('/characters', methods=['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token

    characters = Character.query.filter_by(user_token=owner).all()

    response = characters_schema.dump(characters)
    return jsonify(response)

# Retrieve ONE Character
@api.route('/characters/<id>', methods=['GET'])
@token_required
def get_character(current_user_token, id):
    character = Character.query.get(id)

    response = character_schema.dump(character)
    return jsonify(response)

# Update a Character
@api.route('/characters/<id>', methods=['POST', 'PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.race = request.json['race']

    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# Delete a Character
@api.route('/characters/<id>', methods=['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)

    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)