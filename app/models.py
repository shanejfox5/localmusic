from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

'''
artist, venue, event, and join table have their own classes 
'''
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)
    hometown = db.Column(db.String(120), index=True)
    description = db.Column(db.String(120), index=True)

    events = db.relationship('ArtistToEvent', back_populates='artist', lazy=True)
    '''
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    '''


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    venueID = db.Column(db.Integer, db.ForeignKey('venue.id'))

    artists = db.relationship('ArtistToEvent', back_populates='event', lazy=True)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(140), index=True)
    city = db.Column(db.String(140), index=True)
    state = db.Column(db.String(140), index=True)
    capacity = db.Column(db.Integer, index=True)
    events = db.relationship('Event', backref='venue', lazy=True)


class ArtistToEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artistID = db.Column(db.Integer, db.ForeignKey('artist.id'))
    eventID = db.Column(db.Integer, db.ForeignKey('event.id'))
    artist = db.relationship('Artist', backref='event', lazy=True)
    event = db.relationship('Event', backref='artist', lazy=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
