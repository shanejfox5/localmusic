from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit!')