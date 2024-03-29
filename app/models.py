from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

challengers = db.Table('challengers',
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

winners = db.Table('winners',
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

creator = db.Table('creator',
        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


#NEEDING Delete Option
class User(UserMixin, db.Model):

    __tablename__ = 'user'
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
            ).count() > 0

    def set_coins(self, user, amount):
        self.coins = amount 

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now())
    coins = db.Column(db.Integer, default=10)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')


#NEEDING Delete Option
class Event(db.Model):

    __tablename__ = 'event'

    def __repr__(self):
        return '<Event {}>'.format(self.eventname)

    def add_challenger(self, user):
        self.challengers.append(user)

    def add_winner(self, user):
        self.winners.append(user)

    def add_creator(self, user):
        self.creator.append(user)

    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(64), index=True, unique=True)
    time_to_bet = db.Column(db.DateTime)
    description = db.Column(db.String(250))
    amount = db.Column(db.Integer)
    winsetted = db.Column(db.Boolean, default=False)
    betting_quote = db.Column(db.String(30))
    posts = db.relationship('Post', backref='title')

    winners = db.relationship(
        'User', secondary=winners, lazy='subquery',
        backref=db.backref('winners', lazy=True))

    challengers = db.relationship(
        'User', secondary=challengers, lazy='subquery',
        backref=db.backref('challengers', lazy=True))

    creator = db.relationship(
        'User', secondary=creator, lazy='subquery',
        backref=db.backref('creator', lazy=True))

class Post(db.Model):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Bet(db.Model):

    __tablename__ = 'bet'

    def __repr__(self):
        return '<Amount {}>'.format(self.amount)

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow)
    betonloose = db.Column(db.Boolean, default=False)
    amount = db.Column(db.Integer)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', foreign_keys=[user_id])
    winner = db.relationship('User', foreign_keys=[winner_id])
    event = db.relationship('Event', foreign_keys=[event_id])

    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

