import os

base_dir = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = '2e10737dc9d08a4805bf484e01d1e08b'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(base_dir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USER')
    MAIL_PASSWORD = os.getenv('MAIL_PASSW')
