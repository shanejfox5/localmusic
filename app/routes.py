from flask import render_template, flash, redirect, url_for
from app import app, db
from random import randrange
from app.forms import NewArtistForm
from app.models import Artist, ArtistToEvent, Event, Venue
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    '''
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    '''
    return render_template('index.html', title='Home')


@app.route('/quotes')
def quotes():
    quotes = ["'Don't cry because it's over, smile because it happened.' ― Dr. Seuss",
              "'Be yourself; everyone else is already taken.'― Oscar Wilde",
              "'So many books, so little time'- Frank Zappa",
              "'A room without books is like a body without a soul.'- Marcus Julius Cicero",
              "'You know you're in love when you can't fall asleep because reality is finally better than your dreams.'- Dr. Suess",
              "'Be the change that you wish to see in the world.'- Ghandi"
              ]
    quoteChoice = randrange(len(quotes))
    currentQuote = quotes[quoteChoice]
    return render_template('quote.html', title="Quote", quote=currentQuote)


@app.route('/artists')
def artists():
    data = Artist.query.order_by(Artist.name).all()
    return render_template('artists.html', title="Artists", artists=data)


@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
    form = NewArtistForm()
    if form.validate_on_submit():
        flash_message = 'New Artist Created: {}'\
            .format(form.name.data)
        flash(flash_message)
        a = Artist(name=form.name.data, hometown=form.hometown.data, description=form.description.data)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for('artists'))
    return render_template('new_artist.html', title="New Artist", form=form)

'''
@app.route('/artist')
def artist():
    artist_info = {"name": "The Rockers",
                   "description": "They like to rock the house.",
                   "events": ["The Haunt on 9/15", "The State on 10/12"]}
    return render_template('artist.html', title="Artist", artist=artist_info)
'''


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    # now create Artist, Venues, Events, and ArtistToEvent Objects and persist them to the db
    artist1 = Artist(name='Shane Fox', hometown='Delmar', description='He rocks')
    artist2 = Artist(name='Doug Turnbull', hometown='Ithaca', description='He always rocks')
    artist3 = Artist(name='John Doe', hometown='Cortland', description='He never rocks')
    db.session.add_all([artist1, artist2, artist3])
    db.session.commit()
    d1 = datetime(2019, 10, 19, 20, 0)
    event1 = Event(title='Jam Fest', date=d1, venueID=1)
    d2 = datetime(2019, 11, 15, 21, 0)
    event2 = Event(title='Turn up', date=d2, venueID=1)
    d3 = datetime(2019, 12, 5, 19, 0)
    event3 = Event(title='Fun Time', date=d3, venueID=3)
    db.session.add_all([event1, event2, event3])
    db.session.commit()
    venue1 = Venue(title='The Haunt', city='Ithaca', state='New York', capacity=100)
    venue2 = Venue(title='Moonies', city='Ithaca', state= 'New York', capacity=200)
    venue3 = Venue(title='Silky Jones', city='Ithaca', state='New York', capacity=300)
    db.session.add_all([venue1, venue2, venue3])
    db.session.commit()
    a2e1 = ArtistToEvent(artist=artist1, event=event1)
    a2e2 = ArtistToEvent(artist=artist2, event=event1)
    a2e3 = ArtistToEvent(artist=artist3, event=event3)
    a2e4 = ArtistToEvent(artist=artist1, event=event3)
    db.session.add_all([a2e1, a2e2, a2e3, a2e4])
    db.session.commit()
    return render_template('index.html', title='Home')


@app.route('/artist/<artist_name>')
def artist(artist_name):
    a = Artist.query.filter_by(name=artist_name).first()
    return render_template('artist.html', title="Artist", artist=a)
