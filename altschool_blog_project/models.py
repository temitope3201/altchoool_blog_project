import imp
from altschool_blog_project import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))




class User(db.Model,UserMixin):

    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpeg')
    password = db.Column(db.String(60), nullable = False)
    post = db.relationship('Post', backref = 'author', lazy=True)

    def get_reset_token(self, expires_sec = 1800):

        s = Serializer(app.config['SECRET_KEY'], expires_sec)

        return  s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']

        except:
            return None
        
        return User.query.get(user_id)

    def __repr__(self) -> str:
        return f'This is User {self.username}, with email {self.email}'

class Post(db.Model):

    __tablename__ = 'post'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
   
    def __repr__(self) -> str:
        return f'This is post {self.title}, posted on  {self.date_posted}'

class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), nullable = False)
    message = db.Column(db.String(), nullable = False)

    def __repr__(self) -> str:
        return f"This is a message from {self.name}, with email {self.email} and a message of {self.message}  "
