# An application about recording favorite songs & info

import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
# from flask_moment import Moment # needs pip/pip3 install flask_moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
# from flask_sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Date, Time
# from flask_sqlalchemy import relationship, backref

# from flask_migrate import Migrate, MigrateCommand # Later

# Configure base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

# Application configurations
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstringfromsi364thisisnotsupersecurebutitsok'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite') # Determining where your database file will be stored, and what it will be called
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff
manager = Manager(app)
# moment = Moment(app) # For time # Later
db = SQLAlchemy(app) # For database use
# migrate = Migrate(app, db) # For database use # later

#########
######### Everything above this line is important setup, not problem-solving.
#########

##### Set up Models #####

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique=True) # Only unique title songs
    artist = db.Column(db.String(64))
    genre = db.Column(db.String(64))

    def __repr__(self):
        return "{} by {} | {}".format(self.title,self.artist, self.genre)

##### Set up Forms #####

class SongForm(FlaskForm):
    song = StringField("What is the title of your favorite song?", validators=[Required()])
    artist = StringField("What is the name of the artist who performs it?",validators=[Required()])
    # Add a line in the form to ask for the genre of the song, which should be required
    submit = SubmitField('Submit')

##### Helper functions

### For database additions / get_or_create
def get_or_create_song(db_session, song_title, song_artist, song_genre):
    # Query for the song based on its title
    # If it exists already, return the Song object
    # Otherwise,
    # Create a row in the Song table with this data
    # Add it and commit it to the db
    # Return the song object from the function, no matter what


##### Set up Controllers (view functions) #####

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

## Main route

@app.route('/', methods=['GET', 'POST'])
def index():
    songs = Song.query.all()
    num_songs = len(songs)
    form = SongForm()
    if form.validate_on_submit():

        # Check if there already is a song with that title
        # And if so, flash a message that they've already saved a song with that title!
        # (The flashed message is already set up in the template)

        # Invoke the get_or_create function above to save a song with the data from the form

        return redirect(url_for('see_all'))
    return render_template('index.html', form=form,num_songs=num_songs) 

@app.route('/all_songs')
def see_all():
    all_songs = [] # To be tuple list of title, genre
    songs = Song.query.all()
    for s in songs:
        all_songs.append((s.title,s.artist, s.genre))
    # Add a return statement so that the corret data will be sent to the all_songs.html template!


if __name__ == '__main__':
    db.create_all() # Creates database tables on run -- if you run one of the ways described below!
    manager.run() # NEW: run with this: python main_app.py runserver (or app.run() if you get an error)
    # Also provides more tools for debugging
