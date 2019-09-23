from flask import render_template, flash, redirect, url_for
from app import app
from random import randrange
from app.forms import NewArtistForm

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
              "'A room without books is like a body without a soul.'- Marcus Tullius Cicero",
              "'You know you're in love when you can't fall asleep because reality is finally better than your dreams.'- Dr. Suess",
              "'Be the change that you wish to see in the world.'- Ghandi"
              ]
    quoteChoice = randrange(len(quotes))
    currentQuote = quotes[quoteChoice]
    return render_template('quote.html', title="Quote", quote=currentQuote)


@app.route('/artists')
def artists():
    data = [{'artist': 'X Ambassadors'}, {'artist': 'Gunpoets'}, {'artist': 'Donna the Buffalo'},
            {'artist': 'The Blind Spots'}]
    return render_template('artists.html', title="Artists", artists=data)


@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
    form = NewArtistForm()

    if form.validate_on_submit():

        flash_message = 'New Artist Created: {}'\
            .format(form.name.data)
        flash(flash_message)

        return render_template('my_new_artist.html', title='New Artist', name=form.name.data, hometown=form.hometown.data, description=form.description.data)

    return render_template('new_artist.html', title="New Artist", form=form)


@app.route('/artist')
def artist():
    artist_info = {"name": "The Rockers",
                   "description": "They like to rock the house.",
                   "events": ["The Haunt on 9/15", "The State on 10/12"]}
    return render_template('artist.html', title="Artist", artist=artist_info)

