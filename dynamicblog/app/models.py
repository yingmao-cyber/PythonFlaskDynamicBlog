from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    # UserMixin gives three property is_authenticated, is_active, is_anonymous and a method get_id()
    # flask login would use id (because it has set to be primary key) to differentiate different users in the session
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128)) # store hash value for password for security reason
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        # generate a hash for password; password will be converted to a hash value
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        # md5 create a hash and hexdigest convert hash to hex
        # d=identicon refers to geometric shape, every time it will generate a different geometric shape
        # md5 can only accept bytes, that is why it is required to use encode to convert it to byte
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime(128), index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    print("loding user from database into memory session...")
    # this is used to identify whether user is a new user; it is used to load user records into server session
    # if user does not exist in memory, it would tell flask to load user from db.
    return User.query.get(int(id))
