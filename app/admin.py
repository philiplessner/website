from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from . import db
from .forms import LoginForm, SignupForm

admin = Blueprint('admin', __name__)

@admin.route('/login')
def login():
    form = LoginForm()
    return render_template('login2.html', form=form)

@admin.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        stmt = db.select(User).where(User.email == form.email.data)
        user = db.session.scalars(stmt).first()

    if not user or not check_password_hash(user.password_hash, form.password.data):
        flash('Please check your login details and try again.')
        return redirect(url_for('admin.login'))

    login_user(user, remember=form.remember_me.data)
    return redirect(url_for('admin.profile'))

@admin.route('/signup')
@login_required
def signup():
    form = SignupForm()
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))
    return render_template('signup2.html', form=form)

@admin.route('/signup', methods=['POST'])
def signup_post():
    #email = request.form.get('email')
    #name = request.form.get('name')
    #password = request.form.get('password')
    form = SignupForm()
    stmt = (db.select(User.email)
            .select_from(User)
            .where(User.email==form.email.data))
    user = db.session.execute(stmt).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('admin.login'))

    new_user = User(email=form.email.data, name=form.name.data, password_hash=generate_password_hash(form.password.data))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('admin.login'))

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@admin.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('admin.login'))

    return render_template('profile.html', name=current_user.name)