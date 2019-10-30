from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms.fields.html5 import DateField


class NewArtistForm(FlaskForm):
    name = StringField('Artist Name', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit!')


class NewVenueForm(FlaskForm):
    title = StringField('Venue Name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    capacity = IntegerField('Capacity')
    submit = SubmitField('Submit!')


class NewEventForm(FlaskForm):
    title = StringField('Event Name', validators=[DataRequired()])
    date = DateField('Start Time', format='%Y-%m-%d')
    venueID = SelectField('venueID', coerce=int, choices=[], validators=[DataRequired()])
    artists = SelectMultipleField('Artists', coerce=int, choices=[], option_widget=None)
    submit = SubmitField('Submit!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

