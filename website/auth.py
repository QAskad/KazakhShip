from flask import Blueprint, render_template, request, flash, get_flashed_messages, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from email_validator import validate_email, EmailNotValidError
import dns.resolver


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:  # Сравниваем пароли без хэширования
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Try again.', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        try:
            valid = validate_email(email)
            email = valid.email

            domain = email.split('@')[1]
            try:
                dns.resolver.resolve(domain, 'MX')
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                flash(f"The domain {domain} is invalid", category='error')
                return redirect(url_for('auth.sign_up'))

        except EmailNotValidError as e:
            flash(str(e), category='error')
            return redirect(url_for('auth.sign_up'))

        user = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()

        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('Name must be greater than 1 character', category='error')
        elif len(username) < 3:
            flash('Username must be greater than 2 character', category='error')
        elif existing_username:
            flash('Username already exists', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 5 characters', category='error')
        else:
            new_user = User(email=email, first_name=first_name, username=username, password=password1, image_file='default.jpg')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


@auth.route('/account/update', methods=['GET', 'POST'])
@login_required
def update_account():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password1 = request.form.get('password1')
        new_password2 = request.form.get('password2')
        profile_image = request.form.get('profile_image')

        if new_username and new_username != current_user.username:
            existing_username = User.query.filter_by(username=new_username).first()
            if existing_username:
                flash('Username already exists', category='error')
            elif len(new_username) < 3:
                flash('Username must be greater than 2 characters', category='error')
            else:
                current_user.username = new_username

        if new_password1 and new_password1 != new_password2:
            flash('Passwords do not match', category='error')
        elif new_password1 and len(new_password1) < 5:
            flash('Password must be at least 5 characters', category='error')
        elif new_password1:
            current_user.password = new_password1 

        if profile_image:
            current_user.image_file = profile_image

        if not any([flash_message for flash_message in get_flashed_messages()]):
            db.session.commit()
            flash('Account updated successfully', category='success')
            return redirect(url_for('auth.account'))

    return render_template("update_account.html", user=current_user)
