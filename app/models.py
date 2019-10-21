from datetime import datetime
from app import db

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
