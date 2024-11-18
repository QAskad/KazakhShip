from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user
from .models import User
from . import db

website_bp = Blueprint('website_bp', __name__)

# Home route
@website_bp.route('/')
def home():
    return render_template('home.html')

# Account route (view account)
@website_bp.route('/account')
@login_required
def account():
    return render_template('account.html')

# Admin route (admin dashboard)
@website_bp.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

# Library route (library page)
@website_bp.route('/library')
@login_required
def library():
    return render_template('library.html')

# Login route (login page)
@website_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return redirect(url_for('website_bp.login'))

        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # Сравниваем пароли напрямую
            flash('Logged in successfully', category='success')
            login_user(user, remember=True)
            return redirect(url_for('website_bp.home'))
        else:
            flash('Invalid username or password', category='error')

    return render_template('login.html')

# Sign-up route (sign-up page)
@website_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('website_bp.sign_up'))
        
        # Проверяем, существует ли пользователь с таким email
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', 'error')
            return redirect(url_for('website_bp.sign_up'))
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully', category='success')
        return redirect(url_for('website_bp.login'))  # Направляем на страницу входа

    return render_template('sign_up.html')

# Update account route (update user account info)
@website_bp.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_password = request.form.get('password')

        if new_username:
            current_user.username = new_username
        if new_password:
            current_user.password = new_password

        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('website_bp.account'))
    
    return render_template('update_account.html')

# Upload route (upload file page)
@website_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'error')
            return redirect(url_for('website_bp.upload'))

        file = request.files['file']
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(url_for('website_bp.upload'))

        flash(f'File "{file.filename}" uploaded successfully!', 'success')
        return redirect(url_for('website_bp.library'))
    return render_template('upload.html')
