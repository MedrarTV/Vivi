# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField, TextField, SelectMultipleField, DateField, BooleanField
from wtforms.validators import Required, Length, DataRequired, Optional

#from wtforms.fields.html5 import DateField
import csv


class InputForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):        
        super(InputForm, self).__init__(*args,**kwargs) 
        self.venue.choices = self.fill_dict('venues',['ven_short','venue'])
        self.artists.choices = self.fill_dict('people',['name','categories'])
        self.curator.choices = self.fill_dict('people', ['name', 'categories'])
        self.inst.choices = self.fill_dict('venues',['venue'])
        self.videographer.choices = self.fill_dict('videographers',['vid_short','videographer'])
        self.categories.choices = self.fill_dict('categories',['category'])
        self.interviewer.choices = self.fill_dict('people', ['name','categories'])
        self.title_of_edited_video.choices = self.fill_dict('title_of_edited_videos',['title'])
        self.keywords.choices = self.fill_dict('keywords',['keyword'])   
        self.featuring.choices = self.fill_dict('people', ['name','categories'])
        self.topics.choices = self.fill_dict('topics',['topic'])

    def fill_dict(self,dict_name,ids=[]):
        choices = [(None, '')]
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
    event_title = StringField('Event Title *', validators=[DataRequired(),Length(max=170)])
    event_title_ar = StringField('Event Title AR')

    current_date = DateField('Shooting Date *',format='%d-%m-%Y' ,validators=[DataRequired()])
    unkn_date = BooleanField('Unknown Date')

    event_date = DateField('Event Date', format='%d-%m-%Y', validators=[Optional()])
    event_date_until = DateField('Until', format='%d-%m-%Y',validators=[Optional()])

    ## ONE FIELD ONLY
    videographer = SelectField('Videographer *', validators=[DataRequired()])

    ## ONE FIELD ONLY
    venues_list = [(1,'aa'),(2,'bb'),(3,'cc'),(4,'dd'),(5,'tt'),(6,'ff')]

    venue = SelectField('Venue *', validators=[DataRequired()], choices= venues_list)


    ## ONE OR MORE FIELDS
    artists = SelectMultipleField('Artists')
    
    credits = TextAreaField('Credits')
    credits_ar = TextAreaField('Credits AR')

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

    cam_aud = SelectField('Camera /Audio *', choices=[('1','C1'), ('2','C2'), ('3','C3'), ('4','A1'), ('5','A2'), ('6','A3')] ,validators=[DataRequired()])

    edited=None

    submit = SubmitField('Submit')



