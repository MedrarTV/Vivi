from flask import Flask, render_template, session, redirect, url_for, jsonify, request, Response
from flask_script import Manager
from flask_bootstrap import Bootstrap
from input_form import InputForm
import json
import os
from add_item import ArtistForm, VenueForm, ShooterForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vtrardem'
app.config['DEBUG'] = True
app.config['WTF_CSRF_ENABLED'] = False
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

        dictionaries/venues.csv , venues_dict, venue, inst [ven_id,inst_ids]

        dictionaries/creative_people.csv , people_dict, artists, curator, interviewer [aids,cids,iids]

        dictionaries/videographers.csv , videographers_dict, videographer [vid]

        dictionaries/categories.csv , categories_dict, categories [catids]
                
        dictionaries/title_of_edited_videos.csv , title_of_edited_video_dict, title_of_edited_video [tids]

        dictionaries/keywords.csv , keywords_dict, keywords [kids]
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
    form = InputForm(csrf_enabled=False)
    #print(request.form, "\n", session, "\n===================================\n")  # Debugging
    if form.validate_on_submit():
        session['venue'] = form.venue.data
        print('=============session of venue================')
        print(session['venue'])
        return redirect(url_for('add_artist'))
    return render_template('index.html', form=form, venue=session.get('venue'))


@app.route('/add_artist', methods=['GET','POST'])
def add_artist():
    form = ArtistForm(csrf_enabled=False)
    if form.validate_on_submit():
        print('i am here')
        return redirect(url_for('index'))
    return render_template('add_artist.html', form=form)


@app.route('/add_videographer', methods=['GET'])
def add_videographer():
    form = ShooterForm(csrf_enabled=False)
    return render_template('add_videographer.html', form=form)


@app.route('/add_venue', methods=['GET'])
def add_venue():
    form = VenueForm(csrf_enabled=False)
    return render_template('add_venue.html', form=form)

if __name__ == '__main__':
    manager.run()
