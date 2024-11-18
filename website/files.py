from flask import Blueprint, request, render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
import os
import re
from .models import File
from . import db

files = Blueprint('files', __name__)
UPLOAD_FOLDER = 'Upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'epub', 'fb2'}

GENRES = ['Fiction', 'Non-Fiction', 'Science', 'Fantasy', 'Mystery', 'Biography']
SUBGENRES = {
    'Fiction': ['Drama', 'Historical', 'Romance'],
    'Non-Fiction': ['Self-help', 'Memoir', 'Essay'],
    'Science': ['Physics', 'Biology', 'Astronomy'],
    'Fantasy': ['Epic', 'Urban', 'Dark'],
    'Mystery': ['Detective', 'Thriller', 'Crime'],
    'Biography': ['Historical', 'Celebrity', 'Personal']
}

@files.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        
        file = request.files['file']
        description = request.form.get('description')
        genre = request.form.get('genre')
        subgenre = request.form.get('subgenre')

        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)

        if not description or len(description) > 100:
            flash('Description is required and must be less than 100 characters.', category='error')
            return redirect(request.url)
        
        if genre not in GENRES:
            flash('Invalid genre selected.', category='error')
            return redirect(request.url)
        
        if subgenre not in SUBGENRES.get(genre, []):
            flash('Invalid subgenre selected.', category='error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Очистка имени файла (замена неподобающих символов)
            filename = clean_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            new_file = File(
                filename=filename,
                description=description,
                genre=genre,
                subgenre=subgenre,
                uploaded_by=current_user.id
            )
            db.session.add(new_file)
            db.session.commit()

            flash('File uploaded successfully!', category='success')
            return redirect(url_for('files.upload_file'))
    return render_template(
        'upload.html',
        user=current_user,
        genres=GENRES,
        subgenres=SUBGENRES
    )

@files.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    file.download_count += 1  
    db.session.commit()
    return send_from_directory(UPLOAD_FOLDER, file.filename)

def allowed_file(filename):
    # Проверка расширения файла
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_filename(filename):
    # Убираем неподобающие символы, заменяем пробелы на подчеркивания
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)  # Разрешаем только буквы, цифры, точки, дефисы и подчеркивания
    return filename
