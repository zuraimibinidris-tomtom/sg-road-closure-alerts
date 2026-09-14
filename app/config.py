import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    
    # Celery
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # LTA API
    LTA_API_KEY = os.getenv('LTA_API_KEY')
    LTA_ACCOUNT_KEY = os.getenv('LTA_ACCOUNT_KEY')
    LTA_API_BASE_URL = os.getenv('LTA_API_BASE_URL', 'https://datamall2.mytransport.sg')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/road_closures_dev'
    )
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
