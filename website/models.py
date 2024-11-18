from . import db
from sqlalchemy.sql import func
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(150), unique=True, nullable=False) 
    email = db.Column(db.String(150), unique=True, nullable=False)  
    password = db.Column(db.String(256), nullable=False) 
    first_name = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(150), nullable=False, default='default.jpg')
    role = db.Column(db.String(10), nullable=False, default='Reader') 
    created = db.Column(db.DateTime(timezone=True), default=func.now()) 
    is_blocked = db.Column(db.Boolean, default=False)
    blocked_until = db.Column(db.DateTime, nullable=True)

    visits = db.relationship('Visit', backref='user', lazy=True)
    files = db.relationship('File', backref='uploader', lazy=True)

class Visit(db.Model):
    __tablename__ = 'visits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())  

class File(db.Model):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)  
    upload_date = db.Column(db.DateTime(timezone=True), default=func.now())  
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    description = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)  
    subgenre = db.Column(db.String(100), nullable=False) 
    download_count = db.Column(db.Integer, default=0) 

GENRE_CHOICES = [
    "Fiction", "Non-Fiction", "Fantasy", "Science Fiction", "Romance", "Mystery", 
    "Horror", "Thriller", "Biography", "History"
]

SUBGENRE_CHOICES = {
    "Fiction": ["Drama", "Adventure", "Historical"],
    "Fantasy": ["Epic Fantasy", "Dark Fantasy", "Urban Fantasy"],
    "Romance": ["Contemporary", "Historical Romance", "Romantic Suspense"],
    "Mystery": ["Detective", "Cozy Mystery"],
    "Science Fiction": ["Space Opera", "Dystopian", "Cyberpunk"]
}
