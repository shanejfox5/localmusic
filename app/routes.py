from flask import render_template, flash, redirect, url_for, request
from app import app, db
from random import randrange
from app.forms import NewArtistForm, LoginForm, RegistrationForm, NewVenueForm, NewEventForm
from app.models import Artist, ArtistToEvent, Event, Venue, User
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
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


@app.route('/new_venue', methods=['GET', 'POST'])
def new_venue():
    form = NewVenueForm()
    if form.validate_on_submit():
        flash_message = 'New Venue Created: {}'\
            .format(form.title.data)
        flash(flash_message)
        v = Venue(title=form.title.data, city=form.city.data, state=form.state.data, capacity=form.capacity.data)
        db.session.add(v)
        db.session.commit()
        return redirect(url_for('new_venue'))
    return render_template('new_venue.html', title="New Venue", form=form)


@app.route('/new_event', methods=['GET', 'POST'])
def new_event():
    form = NewEventForm()
    form.artists.choices = [(artist.id, artist.name) for artist in Artist.query.all()]
    form.venueID.choices = [(venue.id, venue.title) for venue in Venue.query.all()]
    if form.validate_on_submit():
        e = Event(title=form.title.data, date=form.date.data, venueID=form.venueID.data)
        db.session.add(e)
        db.session.commit()

        for a in form.artists.data:
            artist = Artist.query.get(a)
            a2e = ArtistToEvent(artistID=artist.id, eventID=e.id)
            db.session.add(a2e)
            db.session.commit()

        flash_message = 'New Event Created: {}' \
            .format(form.title.data)
        flash(flash_message)
        return redirect(url_for('new_event'))
    return render_template('new_event.html', title="New Event", form=form)


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
    if a is None:
        return render_template('404.html')
    return render_template('artist.html', title="Artist", artist=a)


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstName.data, lastname=form.lastName.data, username=form.username.data, email=form.email.data, password=form.password1.data, password2=form.password2.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


