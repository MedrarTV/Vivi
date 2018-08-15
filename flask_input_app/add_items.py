# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, DateField, SelectMultipleField, TextField
from wtforms.validators import Required, Length, DataRequired
#from wtforms.fields.html5 import DateField
import csv
from input_form import InputForm
from utilities import Utils

class ArtistForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)
        self.categories.choices = InputForm.fill_dict(self,'categories',['category'])

    def create_artist(name,name_ar,ids,biography,biography_ar,website,dict_name='people'):
        artist_id =0
        categories = Utils.group_dict([int(i) for i in ids],dict_keys=['category'] , dict_name='categories')
        if not ids:
            ids = ''
            categories['category'] = ''
        with open('dictionaries/'+dict_name+'.csv', 'r+', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            artist_id = max(int(item['id']) for item in reader)
            print(artist_id)
            writer = csv.writer(file,delimiter=',')
            writer.writerow([str(int(artist_id)+1),name,name_ar,ids,categories['category'],biography,biography_ar,website])
        return int(artist_id)+1

    #print(create_artist('ss','ssadsadsa'))
    name = StringField('Artist Name *', validators=[DataRequired()])
    name_ar = StringField('اسم الفنان *', validators=[DataRequired()])
    categories = SelectMultipleField('Categories',choices=[('0','')])
    biography = TextAreaField('Artist Biography')
    biography_ar = TextAreaField('السيرة الذاتية للفنان')
    website = StringField('Artist\'s Website')
    submit = SubmitField('Submit')


class ShooterForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(ShooterForm, self).__init__(*args, **kwargs)

    def create_shooter(short_name,name,name_ar):
        artist_id =0
        with open('dictionaries/videographers.csv', 'r+', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            artist_id = max(int(item['id']) for item in reader)
            print(artist_id)
            writer = csv.writer(file,delimiter=',')
            writer.writerow([str(int(artist_id)+1),short_name,name,name_ar])
        return int(artist_id)+1

    shooter_short = StringField('Short Name *', validators=[Required()])
    shooter_name = StringField('Shooter Name *', validators=[DataRequired()])
    shooter_name_ar = StringField('اسم المصور *', validators=[DataRequired()])
    submit = SubmitField('Submit')

class VenueForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)

    def create_venue(venue_short,venue,venue_ar,description='',description_ar='',website=''):
        venue_id = 0
        with open('dictionaries/venues.csv', 'r+', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            venue_id = max(int(item['id']) for item in reader)
            print(venue_id)
            writer = csv.writer(file,delimiter=',')
            writer.writerow([str(int(venue_id)+1), venue_short, venue, description, description_ar, website])
        return int(venue_id)+1

    venue_short = StringField('Short Name *', validators=[Required(), Length(max=50)])
    venue = StringField('Institution/Venue/location Name *',
                        validators=[DataRequired()])
    venue_ar = StringField('إسم المؤسسة/المساحة/الموقع *', validators=[DataRequired()])
    description = StringField('Description')
    description_ar = StringField('وصف المؤسسة أو المكان')
    website = StringField('Website')

    submit = SubmitField('Submit')

class ItemForm():
    def create_single_item(item, dict_name, dict_dir='dictionaries/'):
        item_id = 0
        with open(dict_dir+dict_name+'.csv','r+', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            item_id = max(int(item['id']) for item in reader)
            print(item_id)
            writer = csv.writer(file, delimiter=',')
            writer.writerow([str(int(item_id)+1), item])
        return int(item_id)+1
