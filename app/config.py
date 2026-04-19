import os
import yaml
from datetime import timedelta

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or config['app']['secret_key']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or config['database']['url']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or config['app']['jwt_secret_key']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    DEBUG = config['app'].get('debug', False)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config():
    env = os.environ.get('FLASK_ENV') or 'development'
    return config_map.get(env, DevelopmentConfig)
