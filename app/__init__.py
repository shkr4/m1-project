from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_admin import Admin
import os

# Define the extensions globally
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# admin = Admin()


def create_app():
    app = Flask(__name__)

    # Load configuration
    # app.config.from_object('config.Config')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SECRET_KEY'] = 'secretkey'
    # You can change this to your desired directory
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)  # Migrate needs both app and db
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

#    admin.init_app(app)

    from .models import User, Professionals, Order, Services

    with app.app_context():
        db.create_all()

    # Register Blueprints or routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    admin = Admin(app, name='My Admin Panel', template_mode='bootstrap3')

    from .adminClass import UserAdmin, ProfessionalsAdmin, OrderAdmin, ServicesAdmin
    # Add views to Flask-Admin
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(ProfessionalsAdmin(Professionals, db.session))
    admin.add_view(OrderAdmin(Order, db.session))
    admin.add_view(ServicesAdmin(Services, db.session))

    return app


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))


# from flask_admin import Admin
# import os
#
# app = Flask(__name__)
#
# app.secret_key = '_5#y2L"F4Q8zxec]'
#
# UPLOAD_FOLDER = '/home/vivek/.rmp'  # Ensure this folder exists
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# admin = Admin(app)
# Add administrative views here
