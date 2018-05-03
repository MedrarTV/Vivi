from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FileField, SelectField, TextAreaField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    #dicts
    venues_dict = [('0', 'Medrar'), ('1', 'Mashrabeya'), ('2', 'Room')]
    people_dict = [('0', 'Dia'), ('1', 'Allam'), ('2', 'Tawfig')]
    inistitutions_dict = [('0', 'Ins1'), ('1', 'Ins2'), ('2', 'Ins3')]
    videographers_dict = [('0', 'helmy'), ('1', 'Dia'), ('2', 'Mostafa')]
    events_dict = [('0', 'Roznama'), ('1', 'CVF'), ('2', 'D-CAF')]
    keywords_dict = [('0', 'Word1'), ('1', 'Word2'), ('2', 'Word3')]
    title_of_edited_video_dict = [('0', 'Title1'), ('1', 'Title2'), ('2', 'Title3')]


    #the form's elements by order
    unique_id = StringField('Unique ID', validators=[Required()])

    event_title = StringField('Event Title', validators=[Required()])
    event_title_ar = StringField('Event Title AR', validators=[Required()])

    current_date = DateField('Date', validators=[Required()])
    event_date = DateField('Event Date', validators=[Required()])

    
    venue = SelectField('Venue',choices = venues_dict, validators=[Required()])    
    venue_ar = StringField('Venue AR')
    city = StringField('City')
    city_ar = StringField('City AR')


    artists = SelectField('Artists', choices=people_dict, validators=[Required()])
    artists_ar = StringField('Artists AR')

    credits = StringField('Credits')
    credits_ar = StringField('Credits AR')

    curator = SelectField('Curator / Project Manager', choices= people_dict, validators=[Required()])
    curator_ar = StringField('Curator / Project Manager AR')

    inistitutions = SelectField('Institutions', choices=inistitutions_dict, validators=[Required()])
    inistitutions_ar = StringField('Institutions AR')

    videographer = SelectField('Videographer', choices= videographers_dict, validators=[Required()])
    videographer_ar = StringField('Videographer AR')

    event_desc = TextAreaField('Event Description')
    event_desc_ar = TextAreaField('Event Description AR')
    
    footage_desc = TextAreaField('Footage Description')
    footage_desc_ar = TextAreaField('Footage Description AR')

    event_type = SelectField('Event Type', choices=events_dict, validators=[Required()])
    event_type_ar = StringField('Event Type AR')

    biographies = TextAreaField('Biographies')
    biographies_ar = TextAreaField('Biographies AR')

    notes = TextAreaField('Notes and Comments')

    old_directory = StringField('Old Directory')

    interviewer = SelectField('Interviewer', choices= people_dict, validators=[Required()])
    interviewer_ar = StringField('interviewer AR')

    title_of_edited_video = StringField('Title of the Edited Video', validators=[Required()])
    title_of_edited_video_ar = StringField('Title of the Edited Video', validators=[Required()])

    keywords = SelectField('Keywords', choices=keywords_dict, validators=[Required()])
    keywords_ar = StringField('Keywords AR')

    upload_files = FileField('Upload Files', validators=[Required()])
    
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    manager.run()
