from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, DateField, SelectMultipleField, TextField, SelectMultipleField
from wtforms.validators import Required
#from wtforms.fields.html5 import DateField
import csv

class InputForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):        
        super(InputForm, self).__init__(*args,**kwargs) 
        
    
    '''
    THE MAIN DICT: dictionaries/main_dict.csv
            dictionaries/creative_people.csv
            dictionaries/event_types.csv
            dictionaries/institutions.csv
            dictionaries/keywords.csv
            dictionaries/title_of_edited_videos.csv
            dictionaries/venues.csv
            dictionaries/videographers.csv
    '''

    def fill_dict(dict_name):
        #choices=[(0,'')]
        choices=[]
        fill = []
        with open('dictionaries/'+dict_name+'.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f,delimiter=',')
            for item in reader:
                keys_list = list(item.keys())
                fill.append((item['id'],item[keys_list[1]]))
                temp_vals = ''
                for k in keys_list[1:]:
                    temp_vals += item[k]+';'
                choices.append((item['id'],temp_vals))
        return choices
    ## fill keywords and event types dicts
    def fill_single_dicts(dict_name='keywords'):
        choices = [(0,'')]
        with open('dictionaries/'+dict_name+'.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for item in reader:
                for k in list(item.keys())[1:]:
                    choices.append((item['id'], item[k]))
            print(choices)
        return choices
    
    #fill creative people and videographers
    def fill_peoples_dict(dict_name='creative_people'):
        choices =[(0,'')]
        fill = []
        with open('dictionaries/'+dict_name+'.csv','r', encoding='utf-8') as f:
            reader = csv.DictReader(f,delimiter=',')
            for item in reader:
                keys_list = list(item.keys())
                fill.append((item['id'], item[keys_list[1]]))                            
                #choices.append(item['id'])
                #temp_key = int(item['id'])
                temp_vals = ''
                for k in keys_list[1:]:
                    temp_vals += item[k]+';'                     
                choices.append((item['id'],temp_vals))
                print(item)
                print(item.keys())
            print(choices)
            print(fill)
        return None
    
    #fill edited video
    def fill_edited_video_dict():
        return None

    #fill institutions
    def fill_inst_dict():
        return None

    #fill venues
    def fill_venues_dict():
        return None
    


    #class variables
    separator = ';'

    #dicts
    venues_dict = fill_dict('venues')
    people_dict = fill_dict('people')
    institutions_dict = fill_dict('institutions')
    videographers_dict = fill_dict('videographers')
    events_dict = fill_dict('event_types')
    keywords_dict = fill_dict('keywords')
    title_of_edited_video_dict = fill_dict('title_of_edited_videos')    
    
    #the form's elements by order
    unique_id = StringField('Unique ID', validators=[Required()])

    event_title = StringField('Event Title', validators=[Required()])
    event_title_ar = StringField('Event Title AR', validators=[Required()])

    current_date = DateField('Date',format='%Y-%m-%d' ,validators=[Required()])
    event_date = DateField(
        'Event Date', format='%Y-%m-%d', validators=[Required()])


    ## ONE FIELD ONLY
    venue = SelectField('Venue', choices=venues_dict, id='venue')

    selected_venue = TextAreaField(
        'Selected Venue', id='selected_venue', validators=[Required()], render_kw={'readonly': True})


    ## ONE OR MORE FIELDS
    artists = StringField('Artists',
                          validators=[Required()])
    #artists_ar = StringField('Artists AR', render_kw={'readonly': True})
    selected_artists = TextAreaField(
        'Selected Artist(s)', render_kw={'readonly': True})

    credits = StringField('Credits')
    credits_ar = StringField('Credits AR')

    ## ONE OR MORE FIELDS
    curator = SelectField('Curator / Project Manager',
                          choices=people_dict, validators=[Required()])
    selected_curators = TextAreaField(
        'Selected Curator(s)', render_kw={'readonly': True})

    ## ONE OR MORE FIELDS
    inst = SelectField(
        'Institution', choices=institutions_dict, validators=[Required()])
    selected_institutions = TextAreaField(
        'Selected Institution(s)', render_kw={'readonly': True})

    ## ONE FIELD ONLY
    videographer = SelectField(
        'Videographer', choices=videographers_dict, validators=[Required()])

    event_desc = TextAreaField('Event Description')
    event_desc_ar = TextAreaField('Event Description AR')

    footage_desc = TextAreaField('Footage Description')
    footage_desc_ar = TextAreaField('Footage Description AR')

    ## ONE OR MORE FIELDS
    # ONLY ONE COLUMN, AR AND EN
    event_type = SelectField(
        'Event Type', choices=events_dict, validators=[Required()])
    selected_events = TextAreaField(
        'Selected Event(s)', render_kw={'readonly': True})

    biographies = TextAreaField('Biographies')
    biographies_ar = TextAreaField('Biographies AR')

    notes = TextAreaField('Notes and Comments')

    old_directory = StringField('Old Directory')

    ## ONE OR MORE FIELDS
    interviewer = SelectField(
        'Interviewer', choices=people_dict, validators=[Required()])
    selected_interviewers = TextAreaField(
        'Selected Interviewer(s)', render_kw={'readonly': True})

    ## ONE OR MORE FIELDS
    title_of_edited_video = SelectField(
        'Title of the Edited Video', choices=title_of_edited_video_dict, validators=[Required()])
    selected_titles = TextAreaField(
        'Selected Title(s)', render_kw={'readonly': True})

    ## ONE OR MORE FIELDS
    # ONLY ONE COLUMN, AR AND EN
    keywords = SelectMultipleField(
        'Keywords', choices=keywords_dict, validators=[Required()])
    selected_keywords = TextAreaField(
        'Selected Keyword(s)', render_kw={'readonly': True})

    upload_files = FileField('Upload Files', validators=[Required()])

    edited=None

    name = StringField('What is your name?', validators=[Required()], id='name')
    submit = SubmitField('Submit')



