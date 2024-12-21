import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'segretissima')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', '5000')
    DOMAIN = os.getenv('DOMAIN', 'http://localhost:{port}').format(port=PORT)
