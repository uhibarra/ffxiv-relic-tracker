from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user, login_required

from relic_tracker.forms import UserRegisterForm, UserLoginForm
from relic_tracker.models import User, db, check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    email = None
    form = UserRegisterForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = User.query.filter_by(email=form.email.data).first()
            if email is None:
                email = form.email.data
                password = form.password.data

                # Add User into Database
                user = User(email, password=password)
                db.session.add(user)
                db.session.commit()

                flash(f'User created: {email}', 'user-created')
                return redirect(url_for('auth.signin'))

            else:
                flash('Email already exists', 'create-failed')
                return redirect(url_for('auth.signup'))

    except:
        raise Exception('Invalid Form Data: Please check your form.')

    return render_template('signup.html', 
        form = form,
        email = email)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    form.validate
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            # Query user table for users with this info
            logged_user = User.query.filter_by(email=email).first()

            # Check if logged_user exists and password == password
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('Login success', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Incorrect email/password', 'auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Please check your form.')

    return render_template('signin.html', form=form)

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('site.home'))