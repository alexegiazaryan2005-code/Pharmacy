import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'ваш-секретный-ключ-для-безопасности'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pharmacy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
