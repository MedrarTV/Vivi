from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, FileField, SelectField, TextAreaField
from wtforms.validators import Required


class InputForm(FlaskForm):
    #dicts
    venues_dict = [('0', 'Medrar'), ('1', 'Mashrabeya'), ('2', 'Room')]
    people_dict = [('0', 'Dia'), ('1', 'Allam'), ('2', 'Tawfig')]
    institutions_dict = [('0', 'Ins1'), ('1', 'Ins2'), ('2', 'Ins3')]
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


    ## ONE FIELD ONLY
    venue = SelectField('Venue', choices=venues_dict, validators=[Required()])
    venue_ar = StringField('Venue AR', render_kw={'readonly': True})
    city = StringField('City', render_kw={'readonly': True})
    city_ar = StringField('City AR', render_kw={'readonly': True})
    selected_venue = StringField(
        'Selected Venue', render_kw={'readonly': True})

    ## ONE OR MORE FIELDS
    artists = SelectField('Artists', choices=people_dict,
                          validators=[Required()])
    artists_ar = StringField('Artists AR', render_kw={'readonly': True})
    selected_artists = TextAreaField(
        'Selected Artist(s)', render_kw={'readonly': True})

    credits = StringField('Credits')
    credits_ar = StringField('Credits AR')

    ## ONE OR MORE FIELDS
    curator = SelectField('Curator / Project Manager',
                          choices=people_dict, validators=[Required()])
    curator_ar = StringField(
        'Curator / Project Manager AR', render_kw={'readonly': True})
    selected_curators = TextAreaField(
        'Selected Curator(s)', render_kw={'readonly': True})

    ## ONE OR MORE FIELDS
    inistitution = SelectField(
        'Institution', choices=institutions_dict, validators=[Required()])
    inistitution_ar = StringField(
        'Institution AR', render_kw={'readonly': True})
    country = StringField(
        'Country', render_kw={'readonly': True})
    country_ar = StringField(
        'Country AR', render_kw={'readonly': True})
    selected_institutions = TextAreaField(
        'Selected Institution(s)', render_kw={'readonly': True})

    ## ONE FIELD ONLY
    videographer = SelectField(
        'Videographer', choices=videographers_dict, validators=[Required()])
    videographer_ar = StringField(
        'Videographer AR', render_kw={'readonly': True})
    selected_videographer = StringField(
        'Selected Videographer', render_kw={'readonly': True})

    event_desc = TextAreaField('Event Description')
    event_desc_ar = TextAreaField('Event Description AR')

    footage_desc = TextAreaField('Footage Description')
    footage_desc_ar = TextAreaField('Footage Description AR')

    ## ONE OR MORE FIELDS
    event_type = SelectField(
        'Event Type', choices=events_dict, validators=[Required()])
    event_type_ar = StringField('Event Type AR', render_kw={'readonly': True})
    selected_events = TextAreaField(
        'Selected Event(s)', render_kw={'readonly': True})

    biographies = TextAreaField('Biographies')
    biographies_ar = TextAreaField('Biographies AR')

    notes = TextAreaField('Notes and Comments')

    old_directory = StringField('Old Directory')

    ## ONE OR MORE FIELDS
    interviewer = SelectField(
        'Interviewer', choices=people_dict, validators=[Required()])
    interviewer_ar = StringField(
        'interviewer AR', render_kw={'readonly': True})
    selected_interviewers = TextAreaField(
        'Selected Interviewer(s)', render_kw={'readonly': True})

    ## ONE OR MORE FIELDS
    ##title_of_edited_video = SelectField(
      ##  'Title of the Edited Video', choices=title_of_edited_video_dict, validators=[Required()])
    title_of_edited_video_ar = StringField(
        'Title of the Edited Video AR', render_kw={'readonly': True})
    selected_titles = TextAreaField(
        'Selected Title(s)', render_kw={'readonly': True})

    ## ONE OR MORE FIELDS
    keywords = SelectField(
        'Keywords', choices=keywords_dict, validators=[Required()])
    keywords_ar = StringField('Keywords AR', render_kw={'readonly': True})
    selected_keywords = TextAreaField(
        'Selected Keyword(s)', render_kw={'readonly': True})

    upload_files = FileField('Upload Files', validators=[Required()])

    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')