from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField, TextField, SelectMultipleField
from wtforms.validators import Required, Length, DataRequired, Optional
from wtforms.fields.html5 import DateField
import csv

class InputForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):        
        super(InputForm, self).__init__(*args,**kwargs) 
        self.venue.choices = self.fill_dict('venues')
        self.artists.choices = self.fill_dict('people',['name'])
        self.curator.choices = self.fill_dict('people', ['name'])
        self.inst.choices = self.fill_dict('venues',['venue'])
        self.videographer.choices = self.fill_dict('videographers')
        self.categories.choices = self.fill_dict('categories')
        self.interviewer.choices = self.fill_dict('people', ['name'])
        self.title_of_edited_video.choices = self.fill_dict('title_of_edited_videos',['title'])
        self.keywords.choices = self.fill_dict('keywords')   
        self.featuring.choices = self.fill_dict('people', ['name'])
        self.topics.choices = self.fill_dict('topics')
        
        #print(self.fill_dict('venues')) 
        
    
    '''
    THE MAIN DICT: dictionaries/main_dict.csv
            dictionaries/creative_people.csv
            dictionaries/categories.csv
            dictionaries/keywords.csv
            dictionaries/title_of_edited_videos.csv
            dictionaries/venues.csv
            dictionaries/videographers.csv
    '''
    def fill_dict(self,dict_name,ids=[]):
        #choices=[(0,'')]
        choices=[]
        with open('dictionaries/'+dict_name+'.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f,delimiter=',')
            for item in reader:
                keys_list = list(item.keys())
                if not ids:
                    ids=keys_list
                temp_vals = ''
                for k in keys_list[1:]:
                    if(k in ids):                        
                        temp_vals += item[k]+'  '
                choices.append((item['id'],temp_vals))
        return choices
    
    ''' def get_valid_filename(s):
        s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s) '''

    #class variables
    separator = ';'

    #the form's elements by order
    root_dir = StringField('Root Directory *', validators=[DataRequired()])
    event_title = StringField('Event Title *', validators=[DataRequired(),Length(max=120)])
    event_title_ar = StringField('Event Title AR')

    current_date = DateField('Shooting Date *',format='%Y-%m-%d' ,validators=[DataRequired()])
    event_date = DateField('Event Date', format='%Y-%m-%d',validators=[Optional()])
    event_date_until = DateField('Until', format='%Y-%m-%d',validators=[Optional()])

    ## ONE FIELD ONLY
    videographer = SelectField('Videographer *', validators=[DataRequired()])

    ## ONE FIELD ONLY
    venue = SelectField('Venue *', validators=[DataRequired()])

    ## ONE OR MORE FIELDS
    artists = SelectMultipleField('Artists')
    
    credits = StringField('Credits')
    credits_ar = StringField('Credits AR')

    ## ONE OR MORE FIELDS
    curator = SelectMultipleField('Curator / Project Manager')

    ## ONE OR MORE FIELDS
    inst = SelectMultipleField('Institution')


    event_desc = TextAreaField('Event Description')
    event_desc_ar = TextAreaField('Event Description AR')

    footage_desc = TextAreaField('Footage Description')
    footage_desc_ar = TextAreaField('Footage Description AR')

    ## ONE OR MORE FIELDS
    # ONLY ONE COLUMN, AR AND EN
    categories = SelectMultipleField('Categories')

    notes = TextAreaField('Archive Notes')

    old_directory = StringField('Old Directory')

    ## ONE OR MORE FIELDS
    interviewer = SelectMultipleField('Interviewer')

    ## ONE OR MORE FIELDS
    featuring = SelectMultipleField('Featuring')

    ## ONE OR MORE FIELDS
    title_of_edited_video = SelectMultipleField('Title of the Edited Video')

    ## ONE OR MORE FIELDS
    # ONLY ONE COLUMN, AR AND EN
    keywords = SelectMultipleField('Keywords')

    topics = SelectMultipleField('Topics')

    cam_aud = SelectField('Camera /Audio *', choices=[('1','C-1'), ('2','C-2'), ('3','C-3'), ('4','A-1'), ('5','A-2'), ('6','A-3')] ,validators=[DataRequired()])

    #upload_files = FileField('Upload Files', validators=[Required()])

    edited=None

    ##name = StringField('What is your name?', id='name')
    submit = SubmitField('Submit')



