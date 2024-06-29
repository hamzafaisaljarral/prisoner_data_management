import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from app.config import DevelopmentConfig, TestingConfig, ProductionConfig

# Import the db object directly from models
from app.models import db

pymysql.install_as_MySQLdb()


def create_app(config_name='development'):  # default to 'development'
    app = Flask(__name__)

    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }

    if config_name not in config_map:
        raise ValueError(f"Invalid configuration name '{config_name}'. Expected one of: {list(config_map.keys())}")

    app.config.from_object(config_map[config_name])

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    from app.routes import main, initialize_routes
    initialize_routes(app)
    app.register_blueprint(main)

    return app

