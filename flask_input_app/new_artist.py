from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, TextAreaField, DateField, SelectMultipleField, TextField
from wtforms.validators import Required
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
    artist_name = StringField('Artist Name', validators=[Required()])
    artist_name_ar = StringField('Artist Name', validators=[Required()])
    submit = SubmitField('Submit')
