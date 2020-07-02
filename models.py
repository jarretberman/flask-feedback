from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls,password,username,email,first_name,last_name):
        """creates a new instance of User with bcrypt password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(password = hashed_utf8,username = username,email = email,first_name = first_name,last_name = last_name)

    @classmethod
    def authenticate(cls,username,password):
        
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password,password):
            return u
        else:
            return False

    def change_password(self,password):

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        self.password = hashed_utf8
        return True

    
class Feedback(db.Model):

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20),db.ForeignKey(User.username, ondelete='cascade'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    user = db.relationship('User',backref='posts')