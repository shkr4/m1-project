from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
#from flask_login import LoginManager
#from flask_admin import Admin
import os

# Define the extensions globally
db = SQLAlchemy()
#migrate = Migrate()
#login_manager = LoginManager()
#admin = Admin()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    #app.config.from_object('config.Config')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')  # You can change this to your desired directory
    #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize extensions with the app
    db.init_app(app)
#    migrate.init_app(app, db)  # Migrate needs both app and db
#    login_manager.init_app(app)
#    admin.init_app(app)

    from .models import User
    
    with app.app_context():
        db.create_all()

    

    # Register Blueprints or routes
    from .routes import main_bp
    app.register_blueprint(main_bp)
    

    return app





#from flask_admin import Admin
#import os
#
#app = Flask(__name__)
#
#app.secret_key = '_5#y2L"F4Q8zxec]'
#
#UPLOAD_FOLDER = '/home/vivek/.rmp'  # Ensure this folder exists
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
#admin = Admin(app)
# Add administrative views here

