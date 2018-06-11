from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField, TextField, SelectMultipleField
from wtforms.validators import Required, Length, DataRequired, Optional
from wtforms.fields.html5 import DateField
import csv


class InputForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):        
        super(InputForm, self).__init__(*args,**kwargs) 
        self.venue.choices = self.fill_dict('venues',['ven_short','venue'])
        self.artists.choices = self.fill_dict('people',['name'])
        self.curator.choices = self.fill_dict('people', ['name'])
        self.inst.choices = self.fill_dict('venues',['venue'])
        self.videographer.choices = self.fill_dict('videographers',['vid_short','videographer'])
        self.categories.choices = self.fill_dict('categories',['category'])
        self.interviewer.choices = self.fill_dict('people', ['name'])
        self.title_of_edited_video.choices = self.fill_dict('title_of_edited_videos',['title'])
        self.keywords.choices = self.fill_dict('keywords',['keyword'])   
        self.featuring.choices = self.fill_dict('people', ['name'])
        self.topics.choices = self.fill_dict('topics',['topic'])
        
        #print(self.fill_dict('venues')) 

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
                        temp_vals += item[k]
                        if(len(ids)>1):
                            temp_vals += ' | '
                choices.append((item['id'],temp_vals))
        return choices
    
    #class variables
    keys_list = ['id', 'root_dir', 'event_title', 'normalized_title', 'event_title_ar', 'current_date', 'event_date', 'event_date_until', 'vid', 'vid_short', 'videographer', 'videographer_ar', 'ven_id', 'ven_short', 'venue', 'venue_ar', 'venue_description', 'venue_description_ar', 'cam_aud', 'aids', 'artists', 'artists_ar', 'credits', 'credits_ar', 'cids', 'curator',
                 'curator_ar', 'iids', 'interviewer', 'interviewer_ar', 'fids', 'featuring', 'featuring_ar',
                 'inst_ids', 'inst', 'inst_ar', 'event_desc', 'event_desc_ar', 'footage_desc', 'footage_desc_ar',
                 'catids', 'categories', 'topids', 'topics', 'kids', 'keywords', 'arch_notes',
                 'tids', 'titles_of_vids', 'titles_of_vids_ar', 'vids_url', 'directory', 'edited']
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



