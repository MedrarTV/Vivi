from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, SelectMultipleField, TextField, SelectMultipleField
from wtforms.validators import Required, Length, DataRequired, Optional
from wtforms.fields.html5 import DateField
import csv
import re
import os
import pandas as pd


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
                        temp_vals += item[k]
                        if(len(ids)>1):
                            temp_vals += ' | '
                choices.append((item['id'],temp_vals))
        return choices
    
    def get_valid_filename(s):
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', s)
    
    def verify_root_path(root_dir):
        return os.path.isdir(root_dir)

    def determine_cam_aud(i):
        cam_aud=''
        if i <= 3:
            cam_aud = 'C-'+i
        else:
            cam_aud = 'A-'+str(i-3)
        return cam_aud
             
    
    def create_dir(form_dict,separator =';'):
        root_dir = form_dict['root_dir']
        cur_date = form_dict['current_date']        
        event_title = InputForm.get_valid_filename(form_dict['event_title'])
        ven_id = form_dict['ven_id']
        vid = form_dict['vid']
        cam_aud = form_dict['cam-aud']
        venue =''
        videographer = ''
        relative_path =''
        
        cam_aud = InputForm.determine_cam_aud(int(cam_aud))
        
        with open('dictionaries/venues.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for item in reader:
                if item['id'] == ven_id:
                    venue = item['venue']
                    break

        with open('dictionaries/videographers.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for item in reader:
                if item['id'] == ven_id:
                    videographer = item['name']
                    break

        relative_path = cur_date[0:4]+separator+event_title+'\\'+cur_date[5:7]+separator+venue+'\\'+cur_date[8:10]+separator+videographer+'\\'+cam_aud

        if(os.path.isdir(root_dir)):
            try:
                os.mkdir(os.path.join(root_dir,relative_path))
                return True
            except FileExistsError as e:
                print("the Directory Already Exists",e)
                return False
    
    def clone_dict(src,dst):
        res = dst
        keys_list = list(set(src.keys()).intersection(dst.keys()))
        for i in keys_list:
            res[i]=src[i]
        return res
    

    def group_dict(ids, dict_keys=['name', 'name_ar'], dict_name='people', dicts_dir='dictionaries/', separator=';'):
        dictionary = pd.read_csv(dicts_dir+dict_name+'.csv')
        res_dict = dict.fromkeys(dict_keys)
        
        for item in res_dict:
            item=[]

        for i in ids:
            temp_dict = dict(dictionary.iloc[i])
            for j in temp_dict.keys():
                if j in dict_keys:
                    res_dict[j].append(temp_dict[j])
        
        for k in res_dict.keys():
            res_dict[k] = separator.join(res_dict[k])

        return res_dict

    def write_new_rec(form_dict,directory,dicts_dir='dictionaries/',edited=0):
        
                           
        title_of_edited_videos = pd.read_csv(dicts_dir+'title_of_edited_videos.csv')

        keys_list = ['id','root_dir','event_title','normalized_title','event_title_ar','current_date'
                    ,'event_date','event_date_until','vid','vid_short','videographer','videographer_ar'
                    ,'ven_id','ven_short','venue','venue_ar','venue_description','venue_description_ar'
                    ,'cam_aud','aids','artists','artitsts_ar','credits','credits_ar','cids','curator',
                    'curator_ar','iids','interviewer','interviewer_ar','fids','featuring','featuring_ar',
                    'inst_ids','inst','inst_ar','event_desc','event_desc_ar','footage_desc','footage_desc_ar',
                    'catids','categories','topids','topics','kids','keywords','arch_notes',
                    'tids','title_of_edited_video','title_of_edited_video_ar','edited_video_url','directory','edited']
        
        main_dict = dict.fromkeys(keys_list)

        main_dict = InputForm.clone_dict(form_dict, main_dict)

        main_dict['id'] = pd.read_csv(dicts_dir+'main_dict.csv').max()['id']+1
        main_dict['normalized_title'] = InputForm.get_valid_filename(
            main_dict['event_title'])
        
        videographer = pd.read_csv(dicts_dir+'videographers.csv')
        videographer = videographer.iloc[main_dict['vid']]
        main_dict['vid_short'] = dict(videographer)['vid_short']
        main_dict['videographer'] = dict(videographer)['name']
        main_dict['videographer_ar'] = dict(videographer)['name_ar']

        venue = pd.read_csv(dicts_dir+'venues.csv')
        venue = dict(venue.iloc[main_dict['ven_id']])
        main_dict = InputForm.clone_dict(venue, main_dict)

        main_dict['cam_aud'] = InputForm.determine_cam_aud(main_dict['cam_aud'])

        artists = InputForm.group_dict(list(main_dict['aids']))
        curators = InputForm.group_dict(list(main_dict['cids']))
        interviewers = InputForm.group_dict(list(main_dict['iids']))
        featuring = InputForm.group_dict(list(main_dict['fids']))

        main_dict['artists'] = artists['name']
        main_dict['artists_ar'] = artists['name_ar']
        main_dict['curators'] = curators['name']
        main_dict['curators_ar'] = curators['name_ar']
        main_dict['interviewers'] = interviewers['name']
        main_dict['interviewers_ar'] = interviewers['name_ar']
        main_dict['featuring'] = featuring['name']
        main_dict['featuring_ar'] = featuring['name_ar']

        venues = InputForm.group_dict(list(main_dict['inst_ids']),['venue','venue_ar'],'venues')

        main_dict['inst'] = venues['venue']
        main_dict['inst_ar'] = venues['venue_ar']

        main_dict['categories'] = InputForm.group_dict(list(main_dict['catids']), ['category'], 'categories')['category']
        main_dict['keywords'] = InputForm.group_dict(list(main_dict['kids']), ['keyword'], 'keywords')['keywords']
        main_dict['topics'] = InputForm.group_dict(list(main_dict['topids']), ['topic'], 'topics')['topics']

        edited_videos = InputForm.group_dict(list(main_dict['tids']), ['title', 'title_ar', 'url'], 'title_of_edited_videos')

        main_dict['titles_of_vids'] = edited_videos['title']
        main_dict['titles_of_vids_ar'] = edited_videos['title_ar']
        main_dict['vids_url'] = edited_videos['url']

        main_dict['directory'] = directory
        main_dict['edited']= edited

        return main_dict
    
    def write_to_dict(keys_list, rec, dict_name='main_dict', dicts_dir='dictionaries/'):
        with open(dicts_dir+dict_name+'.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file,keys_list)
            try:
                writer.writerow(rec)
            except IOError as e:
                print('ERROR >>>> ',e)

                
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



