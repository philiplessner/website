from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import Base

db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    from app import routes, models
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.register_blueprint(routes.bp)

    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'admin.login'
    login_manager.init_app(app)

     # User loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        stmt = db.select(User).where(User.id == int(user_id))
        user = db.session.scalars(stmt).first()
        return user
     #   return User.query.get(int(user_id))
    
    # Register blueprints
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
