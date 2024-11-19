from flask import Blueprint, request, jsonify, current_app, send_file
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from .models import User, File, db
from .schemas import UserSchema, FileSchema

api = Blueprint('api', __name__)

user_schema = UserSchema()
files_schema = FileSchema(many=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx', 'txt'}

# Check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/register', methods=['POST'])
def register():
    # Registration logic
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@api.route('/login', methods=['POST'])
def login():
    # Login logic
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 400

@api.route('/logout', methods=['POST'])
@login_required
def logout():
    # Logout logic
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@api.route('/account/uploads', methods=['GET'])
@login_required
def user_uploads():
    # Get list of user's uploaded files
    files = File.query.filter_by(user_id=current_user.id).all()
    return jsonify(files_schema.dump(files)), 200

@api.route('/files/upload', methods=['POST'])
@login_required
def upload_file():
    # File upload logic
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file is allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # Save the file to the upload folder
        file.save(file_path)

        # Create a new File record in the database
        new_file = File(
            title=filename,  # You can change this to any data you want to save
            user_id=current_user.id
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'file': filename}), 201

    return jsonify({'error': 'File type not allowed'}), 400

@api.route('/files/<int:file_id>/download', methods=['GET'])
@login_required
def download_file(file_id):
    # Logic to download a file
    file = File.query.get_or_404(file_id)
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.title)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    return jsonify({'error': 'File not found'}), 404

