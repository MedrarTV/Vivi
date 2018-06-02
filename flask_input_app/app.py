from flask import Flask, render_template, session, redirect, url_for, jsonify, request, Response
from flask_script import Manager
from flask_bootstrap import Bootstrap
from input_form import InputForm
import json
import os
from new_artist import ArtistForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vtrardem'
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'G:\\work and courses\\Medrar\\uploading_testing\\'

manager = Manager(app)
bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

'''
THE MAIN DICT: 
dictionaries/main_dict.csv 

        dictionaries/venues.csv , venues_dict, venue

        dictionaries/creative_people.csv , people_dict, artists, curator, interviewer

        dictionaries/institutions.csv , institutions_dict, inst

        dictionaries/videographers.csv , videographers_dict, videographer

        dictionaries/event_types.csv , events_dict, event_type
                
        dictionaries/title_of_edited_videos.csv , title_of_edited_video_dict, title_of_edited_video

        dictionaries/keywords.csv , keywords_dict, keywords
'''

NAMES = ["abc", "abcd", "abcde", "abcdef"]
#NAMES = {1:"abc", 2:"abcd", 3:"abcde", 4:"abcdef"}


@app.route('/artists', methods=['POST', 'GET'])
def artists():
    return Response(json.dumps(InputForm.people_dict), mimetype='application/json')

@app.route('/venues_response', methods=['GET'])
def venues_response():
    return request.values.get('')


@app.route('/upload', methods=['POST'])
def upload_file():
    
    print(app.config['UPLOAD_FOLDER'])
    if request.method == 'POST':
        file = request.files['file[]']
        print(file.filename)
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return index()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/new_artist', methods=['GET'])
def new_artist():
    form = ArtistForm()
    return render_template('new_artist.html', form=form)

if __name__ == '__main__':
    manager.run()
