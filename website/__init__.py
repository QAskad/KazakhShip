from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  
import os

db = SQLAlchemy()
login_manager = LoginManager() 

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(24).hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:642324@localhost/ks'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager.init_app(app) 
    login_manager.login_view = 'auth.login'
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  
        return User.query.get(int(user_id))

    from .auth import auth
    from .admin import admin
    from .files import files
    from .routes import website_bp

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(files, url_prefix='/files')
    app.register_blueprint(website_bp, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app
