# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, DateField, SelectMultipleField, TextField
from wtforms.validators import Required, Length, DataRequired
#from wtforms.fields.html5 import DateField
import csv
from input_form import InputForm
class ArtistForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)
        self.categories.choices = InputForm.fill_dict(self,'categories',['category'])

    def create_artist(name,name_ar,dict_name='people'):
        artist_id =0
        with open('dictionaries/'+dict_name+'.csv', 'r+', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            artist_id = max(item['id'] for item in reader)
            print(artist_id)
            writer = csv.writer(file,delimiter=',')
            writer.writerow([str(int(artist_id)+1),name,name_ar])
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

    def create_shooter(name,name_ar):
        artist_id =0
        with open('dictionaries/videographer.csv', 'r+', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            artist_id = max(item['id'] for item in reader)
            print(artist_id)
            writer = csv.writer(file,delimiter=',')
            writer.writerow([str(int(artist_id)+1),name,name_ar])
        return int(artist_id)+1

    shooter_short = StringField('Short Name *', validators=[Required()])
    shooter_name = StringField('Shooter Name *', validators=[DataRequired()])
    shooter_name_ar = StringField('اسم المصور *', validators=[DataRequired()])
    submit = SubmitField('Submit')

class VenueForm(FlaskForm):
    
    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)

    def create_venue(venue,venue_ar='',city='',city_ar='',country='',country_ar='',description=''):
        venue_id = 0
        with open('dictionaries/venues.csv', 'r+', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file, delimiter=',')
            venue_id = max(item['id'] for item in reader)
            print(venue_id)
            writer = csv.writer(file,delimiter=',')
            writer.writerow([str(int(venue_id)+1), venue, venue_ar, city, city_ar, country, country_ar, description])
        return int(venue_id)+1

    venue_short = StringField('Short Name *', validators=[Required()])
    venue = StringField('Institution/Venue/location Name *',
                        validators=[DataRequired(), Length(max=50)])
    venue_ar = StringField('إسم المؤسسة/المساحة/الموقع *', validators=[DataRequired()])
    description = StringField('Description')
    description_ar = StringField('وصف المؤسسة أو المكان')
    website = StringField('Website')

    submit = SubmitField('Submit')
