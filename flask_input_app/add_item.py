from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, DateField, SelectMultipleField, TextField
from wtforms.validators import Required, Length
#from wtforms.fields.html5 import DateField
import csv


class ArtistForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)

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
    artist_name = StringField('', validators=[Required()])
    artist_name_ar = StringField('', validators=[Required()])
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

    #print(create_artist('ss','ssadsadsa'))
    venue = StringField('Venue', validators=[Required(), Length(max=50)])
    venue_ar = StringField('Venue ARA')
    city = StringField('City')
    city_ar = StringField('City ARA')
    country = StringField('Country')
    country_ar = StringField('Country ARA')
    description = StringField('Description')
    submit = SubmitField('Submit')
