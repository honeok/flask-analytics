import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///logs.db'  # 使用 SQLite 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
