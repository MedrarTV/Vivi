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
    #the form's elements by order
    unique_id = StringField('Unique ID', validators=[Required()])

    event_title = StringField('Event Title', validators=[Required()])
    event_title_ar = StringField('Event Title AR', validators=[Required()])

    current_date = DateField('Date', validators=[Required()])
    event_date = DateField('Event Date', validators=[Required()])

    #venue = SelectField('Venue', validators=[Required()])    
    #venue_ar = 
    #city = 
    #city_ar = 

    #artists = SelectField('Artists', validators=[Required()])
    #artists_ar =

    credits = StringField('Credits')
    credits_ar = StringField('Credits AR')

    #curator = SelectField('Curator / Project Manager', validators=[Required()])
    #curator_ar =

    #inistitutions = SelectField('Institutions', validators=[Required()])
    #inistitutions_ar =

    #videographer = SelectField('Videographer', validators=[Required()])
    #videographer_ar =

    event_desc = TextAreaField('Event Description')
    event_desc_ar = TextAreaField('Event Description AR')
    
    footage_desc = TextAreaField('Footage Description')
    footage_desc_ar = TextAreaField('Footage Description AR')

    #event_type = SelectField('Event Type', validators=[Required()])
    #event_type_ar =

    biographies = TextAreaField('Biographies')
    biographies_ar = TextAreaField('Biographies AR')

    notes = TextAreaField('Notes and Comments')

    old_directory = StringField('Old Directory')

    #interviewer = SelectField('Interviewer', validators=[Required()])
    #interviewer_ar =

    title_of_edited_video = StringField('Title of the Edited Video', validators=[Required()])
    title_of_edited_video_ar = StringField('Title of the Edited Video', validators=[Required()])

    #keywords = SelectField('Keywords', validators=[Required()])
    #keywords_ar =

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
