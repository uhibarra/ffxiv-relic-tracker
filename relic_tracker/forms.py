from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, EqualTo

class UserRegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo("confirm", message="Make sure your passwords match!")])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class CreateCharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[InputRequired()])
    race = SelectField('Race', choices=['Hyur', 'Elezen', "Miqo'te", 'Roegadyn', 'Lalafell', 'Au Ra', 'Hrothgar', 'Viera'], validate_choice=True)
    gender = SelectField('Gender', choices=['Male', 'Female'], validate_choice=True)
    submit = SubmitField('Create')

class UpdateCharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[InputRequired()])
    race = SelectField('Race', choices=['Hyur', 'Elezen', "Miqo'te", 'Roegadyn', 'Lalafell', 'Au Ra', 'Hrothgar', 'Viera'], validate_choice=True)
    gender = SelectField('Gender', choices=['Male', 'Female'], validate_choice=True)
    update = SubmitField('Update')

class ARRNewRelicForm(FlaskForm):
    job = SelectField('Select', choices=[('paladin', 'Excalibur'), ('warrior', 'Ragnarok'), ('white_mage', 'Nirvana'), ('scholar', 'Last Resort'), ('monk','Kaiser Knuckles'), ('dragoon', 'Longinus'), ('ninja', 'Sasuke\'s Blades'), ('bard', 'Yoichi Bow'), ('black_mage', 'Lilith Rod'), ('summoner', 'Apocalypse')])
    submit = SubmitField('Start')

class ARRPaladinForm(FlaskForm):
    # Step 1
    timeworn = BooleanField(label='Timeworn Curtana') # Timeworn Curtana, Southern Thanalan > Zahar'ak - x:32 y:18
    mat_weapon = BooleanField(label='Aeolian Scimitar') # Aeolian Scimitar
    materia = BooleanField(label='Battledance Materia III') # (2) Battledance Materia III
    chimera = BooleanField(label='Chimera Defeated') # Defeat Chimera, get Alumina Salts
    amdapor = BooleanField(label='Amdapor Keep Cleared') # Complete the dungeon, get Amdapor Glyph
    beastmen1 = BooleanField(label='Zahar\'ak Lancer') # Zahar'ak Lancer, Southern Thanalan x:27 y:20
    beastmen2 = BooleanField(label='Zahar\'ak Pugilist') # Zahar'ak Pugilist, Southern Thanalan x:23 y:21
    beastmen3 = BooleanField(label='Zahar\'ak Thaumaturge') # Zahar'ak Thaumaturge, Southern Thanalan x:29 y:19
    hydra = BooleanField(label='Hydra Defeated') # Defeat Hydra
    ifrit = BooleanField(label='Ifrit Defeated') # Defeat Ifrit, get White-Hot Ember
    garuda = BooleanField(label='Garuda Defeated') # Defeat Garuda, get Howling Gale
    titan = BooleanField(label='Tital Defeated') # Defeat Titan, get Hyperfused Ore
    oil = BooleanField(label='Radz-at-Han Quenching Oil') # (1) Radz-at-Han Quenching Oil
    
    # Step 2 - to be continued...

    # Submit Button
    submit = SubmitField('Update')