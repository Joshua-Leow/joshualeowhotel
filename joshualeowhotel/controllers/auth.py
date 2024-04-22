from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, request, redirect, render_template, url_for, flash
from models.forms import RegForm, GuestForm
from models.users import User
from __init__ import login_manager

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    registerConfirm = False
    if request.method == 'POST':
        if form.validate():
            existing_user = User.getUser(email=form.email.data)
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='pbkdf2')
                User.createUser(email=form.email.data, password=hashpass, name=form.name.data)
                registerConfirm = True
                return render_template("login.html", form=form, registerConfirm=registerConfirm, panel="Login")
            else:
                if not existing_user['password']:
                    hashpass = generate_password_hash(form.password.data, method='pbkdf2')
                    User.updatePassword(existing_user.email, hashpass)
                    registerConfirm = True
                    return render_template("login.html", form=form, registerConfirm=registerConfirm, panel="Login")
                form.email.errors.append("User already existed")
                render_template('register.html', form=form, panel="Register")

    return render_template('register.html', form=form, panel="Register")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = RegForm()
    registerConfirm = False

    if request.method == 'POST':
        print(request.form.get('checkbox'))
        if form.validate_on_submit():
            check_user = User.getUser(email=form.email.data)
            if check_user and check_user['password']:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    if form.email.data == 'admin@abc.com':
                        return redirect(url_for('booking.upload'))
                    else:
                        return redirect(url_for('booking.bookRoom'))
                else:
                    form.password.errors.append("User Password Not Correct")
            else:
                form.email.errors.append("No Such User")
        else:
            print('form did not validate')
    return render_template("login.html", form=form, registerConfirm=registerConfirm, panel="Login")


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('about'))
