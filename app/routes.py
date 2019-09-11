from flask import render_template
from app import app
from random import randrange

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
    return render_template('quote.html', title="Quote", quote = currentQuote)

@app.route('/artists')
def artists():
    return render_template('artists.html', title="Artists")

@app.route('/new_artist')
def new_artist():
    return render_template('new_artist.html', title="New Artist")

@app.route('/artist')
def artist():
    return render_template('artist.html', title="Artist")