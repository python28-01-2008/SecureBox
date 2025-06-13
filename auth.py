from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from .. import db, bcrypt, login_manager
from ..forms import LoginForm, RegisterForm
from ..models import User
import base64
from cryptography.fernet import Fernet

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        fernet_key = Fernet.generate_key().decode()
        user = User(username=form.username.data, email=form.email.data,
                    password_hash=hashed_pw, fernet_key=fernet_key)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
