from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField, TextField, SelectMultipleField
from wtforms.validators import Required, Length
from wtforms.fields.html5 import DateField
import csv

class InputForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):        
        super(InputForm, self).__init__(*args,**kwargs) 
        self.venue.choices = self.fill_dict('venues')
        self.artists.choices = self.fill_dict('people')
        self.curator.choices = self.fill_dict('people') 
        self.inst.choices = self.fill_dict('venues')
        self.videographer.choices = self.fill_dict('videographers')
        self.event_type.choices = self.fill_dict('event_types')
        self.interviewer.choices = self.fill_dict('people')
        self.title_of_edited_video.choices = self.fill_dict('title_of_edited_videos')
        self.keywords.choices = self.fill_dict('keywords')   
        #print(self.fill_dict('venues')) 
        
    
    '''
    THE MAIN DICT: dictionaries/main_dict.csv
            dictionaries/creative_people.csv
            dictionaries/event_types.csv
            dictionaries/keywords.csv
            dictionaries/title_of_edited_videos.csv
            dictionaries/venues.csv
            dictionaries/videographers.csv
    '''
    def fill_dict(self,dict_name):
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
    

    #class variables
    separator = ';'

    #the form's elements by order

    event_title = StringField('Event Title', validators=[Required(),Length(max=120)])
    event_title_ar = StringField('Event Title AR', validators=[Required()])

    current_date = DateField('Shooting Date',format='%Y-%m-%d' ,validators=[Required()])
    event_date = DateField('Event Date', format='%Y-%m-%d', validators=[Required()])


    ## ONE FIELD ONLY
    venue = SelectField('Venue', validators=[Required()])

    ## ONE OR MORE FIELDS
    artists = SelectMultipleField('Artists', validators=[Required()])
    
    credits = StringField('Credits')
    credits_ar = StringField('Credits AR')

    ## ONE OR MORE FIELDS
    curator = SelectMultipleField('Curator / Project Manager', validators=[Required()])

    ## ONE OR MORE FIELDS
    inst = SelectMultipleField('Institution', validators=[Required()])

    ## ONE FIELD ONLY
    videographer = SelectField('Videographer', validators=[Required()])

    event_desc = TextAreaField('Event Description')
    event_desc_ar = TextAreaField('Event Description AR')

    footage_desc = TextAreaField('Footage Description')
    footage_desc_ar = TextAreaField('Footage Description AR')

    ## ONE OR MORE FIELDS
    # ONLY ONE COLUMN, AR AND EN
    event_type = SelectMultipleField('Event Type', validators=[Required()])

    biographies = TextAreaField('Biographies')
    biographies_ar = TextAreaField('Biographies AR')

    notes = TextAreaField('Notes and Comments')

    old_directory = StringField('Old Directory')

    ## ONE OR MORE FIELDS
    interviewer = SelectMultipleField('Interviewer', validators=[Required()])

    ## ONE OR MORE FIELDS
    title_of_edited_video = SelectMultipleField(
        'Title of the Edited Video', validators=[Required()])

    ## ONE OR MORE FIELDS
    # ONLY ONE COLUMN, AR AND EN
    keywords = SelectMultipleField('Keywords', validators=[Required()])

    cam_aud = SelectField('Camera /Audio', choices=[('1','CAM-1'), ('2','CAM-2'), ('3','CAM-3'), ('4','AUD-1'), ('5','AUD-2'), ('6','AUD-3')] ,validators=[Required()])

    upload_files = FileField('Upload Files', validators=[Required()])

    edited=None

    ##name = StringField('What is your name?', id='name')
    submit = SubmitField('Submit')



