from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from relic_tracker.forms import ARRNewRelicForm, ARRPaladinForm, CreateCharacterForm, UpdateCharacterForm
from relic_tracker.models import ARRPaladin, ARRWeapon, Character, db

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@site.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateCharacterForm()
    name = None
    race = None
    gender = None

    try: 
        if request.method == 'POST' and form.validate_on_submit():
            print(name, race, gender)
            name = form.name.data
            form.name.data = ''
            race = form.race.data
            form.race.data = ''
            gender = form.gender.data
            form.gender.data = ''
            user_token = current_user.token

            character = Character(name, race, gender, user_token)
            db.session.add(character)
            db.session.commit()

            flash(f"Character created!  Welcome, {character.name}!", "character-created")
            return redirect(url_for('site.characters'))

    except:
        raise Exception('Invalid Form Data: Please check your form.')
        
    return render_template('create.html', 
        name = name,
        race = race,
        gender = gender,
        form = form)

@site.route('/characters', methods=['GET', 'POST'])
@login_required
def characters():
    characters = Character.query.order_by(Character.name)
    weapons = ARRWeapon.query.order_by(ARRWeapon.name)
    return render_template('characters.html',
        characters = characters,
        weapons = weapons)

@site.route('/update/<id>', methods=['POST', 'GET'])
@login_required
def update(id):
    form = UpdateCharacterForm()
    character = Character.query.get_or_404(id)

    if request.method == 'POST' and form.validate_on_submit():
        character.name = request.form['name']
        character.race = request.form['race']
        character.gender = request.form['gender']

        try:
            db.session.commit()

            flash(f"{character.name} updated!", "character-updated")
            return redirect(url_for('site.characters'))
        
        except:
            flash("There was an error. Try again.", "char-update-failed")
            return render_template('update.html',
                form = form,
                character = character)
    
    else:
        return render_template('update.html',
                form = form,
                character = character)

@site.route('/delete/<id>')
@login_required
def delete(id):
    character = Character.query.get_or_404(id)

    try:
        db.session.delete(character)
        db.session.commit()

        flash(f'Deleted: {character.name}', 'char-deleted')
        return redirect(url_for('site.characters'))
    
    except:
        flash(f'There was an error. Try again.', 'delete-failed')
        return redirect(url_for('site.characters'))

@site.route('/arr/<id>', methods=['POST', 'GET'])
@login_required
def arr(id):
    form = ARRNewRelicForm()
    character = Character.query.get_or_404(id)
    weapons = ARRWeapon.query.order_by(ARRWeapon.name)

    if request.method == 'POST' and form.validate_on_submit():
        job = form.job.data
        form.job.data = ''
        
        if (job == 'paladin') and ('excalibur' not in weapons):
            weapon = ARRWeapon(id, 'excalibur')
            paladin = ARRPaladin(id)

            db.session.add(weapon)
            db.session.add(paladin)
            db.session.commit()

            flash(f"Tracker started! Let's get that Excalibur!", "weap-update-success")
            return redirect(url_for('site.arr', wep=weapon.name, id=character.id))
        
        else:
            flash(f"You already started that weapon.", "weap-update-failed")
            return redirect(url_for('site.arr'))

    else:    
        return render_template('arr.html',
            form = form,
            character = character,
            weapons = weapons)

@site.route('/arr/<wep>', methods=['POST', 'GET'])
def excalibur(wep, id):
    form = ARRPaladinForm()
    character = Character.query.get_or_404(id)
    weapon = ARRPaladin.query.get(wep)

    if request.method == 'POST' and form.validate_on_submit():
        weapon.timeworn = request.form['timeworn']
        weapon.mat_weapon = request.form['mat_weapon']
        weapon.materia = request.form['materia']
        weapon.chimera = request.form['chimera']
        weapon.amdapor = request.form['amdapor']
        weapon.beastmen1 = request.form['beastmen1']
        weapon.beastmen2 = request.form['beastmen2']
        weapon.beastmen3 = request.form['beastmen3']
        weapon.hydra = request.form['hydra']
        weapon.ifrit = request.form['ifrit']
        weapon.garuda = request.form['garuda']
        weapon.titan = request.form['titan']
        weapon.oil = request.form['oil']

        try:
            db.session.commit()

            flash(f"Tracker updated!", "weap-update-success")
            return render_template('excalibur.html',
                form = form,
                character = character,
                weapon = weapon)
        
        except:
            flash("There was an error. Try again.", "weap-update-failed")
            return render_template('excalibur.html',
                form = form,
                character = character,
                weapon = weapon)

    else:
        return render_template('excalibur.html',
            form = form,
            character = character,
            weapon = weapon)


# def update(id):
#     form = UpdateCharacterForm()
#     character = Character.query.get_or_404(id)

#     if request.method == 'POST' and form.validate_on_submit():
#         character.name = request.form['name']
#         character.race = request.form['race']
#         character.gender = request.form['gender']

#         try:
#             db.session.commit()

#             flash(f"{character.name} updated!", "character-updated")
#             return redirect(url_for('site.characters'))
        
#         except:
#             flash("There was an error. Try again.", "char-update-failed")
#             return render_template('update.html',
#                 form = form,
#                 character = character)
    
#     else:
#         return render_template('update.html',
#                 form = form,
#                 character = character)