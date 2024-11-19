import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:642324@localhost/ks'
    SQLALCHEMY_TRACK_MODIFICATIONS = False