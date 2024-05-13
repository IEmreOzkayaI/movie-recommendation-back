from flask import Flask
from .routes import register_routes
from .models import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    
    return app
