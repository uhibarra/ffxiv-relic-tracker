import uuid
from datetime import datetime
import secrets

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    character = db.relationship('Character', backref='owner', lazy=True)

    def __init__(self, email, id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'User {self.email} has been added to the database'

class Character(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    race = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)
    arr_weapons = db.relationship('ARRWeapon', cascade='all, delete-orphan', backref='owner', lazy=True)
    arr_paladin = db.relationship('ARRPaladin', cascade='all, delete-orphan', backref='owner', lazy=True)

    def __init__(self, name, race, gender, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.race = race
        self.gender = gender
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"Character created: {self.name}"

class ARRWeapon(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    char_id = db.Column(db.String, db.ForeignKey('character.id'), nullable=False)

    def __init__(self, char_id, name, id=''):
        self.id = self.set_id()
        self.char_id = char_id
        self.name = name

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f'Weapon {self.name.title()} added'

class ARRPaladin(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, default='excalibur')
    char_id = db.Column(db.String, db.ForeignKey('character.id'), nullable=False)

    # Step 1 variables
    timeworn = db.Column(db.Boolean, default=False)
    mat_weapon = db.Column(db.Boolean, default=False)
    materia = db.Column(db.Boolean, default=False)
    chimera = db.Column(db.Boolean, default=False)
    amdapor = db.Column(db.Boolean, default=False)
    beastmen1 = db.Column(db.Boolean, default=False)
    beastmen2 = db.Column(db.Boolean, default=False)
    beastmen3 = db.Column(db.Boolean, default=False)
    hydra = db.Column(db.Boolean, default=False)
    ifrit = db.Column(db.Boolean, default=False)
    garuda = db.Column(db.Boolean, default=False)
    titan = db.Column(db.Boolean, default=False)
    oil = db.Column(db.Boolean, default=False)

    def __init__(self, char_id, timeworn=False, mat_weapon=False, materia=False, chimera=False, amdapor=False, beastmen1=False, beastmen2=False, beastmen3=False, 
                hydra=False, ifrit=False, garuda=False, titan=False, oil=False, id=''):
        self.id = self.set_id()
        self.char_id = char_id
        self.timeworn = timeworn
        self.mat_weapon = mat_weapon
        self.materia = materia
        self.chimera = chimera
        self.amdapor = amdapor 
        self.beastmen1 = beastmen1
        self.beastmen2 = beastmen2
        self.beastmen3 = beastmen3
        self.hydra = hydra
        self.ifrit = ifrit
        self.garuda = garuda
        self.titan = titan
        self.oil = oil

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"ARR Job Set: {self.job}"


# Creation of API Schema via the Marshmallow Object
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'race', 'gender']

character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)