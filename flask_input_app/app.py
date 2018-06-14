# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, jsonify, request, Response, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from input_form import InputForm
import json
import os
from add_item import ArtistForm, VenueForm, ShooterForm
from utilities import Utils

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
    if form.validate_on_submit():
        session['event_title'] = form.event_title.data
        session['root_dir'] = form.root_dir.data
        session['event_title_ar'] = form.event_title_ar.data
        session['event_date'] = form.event_date.data
        session['event_date_until'] = form.event_date_until.data
        session['aids'] = form.artists.data
        session['cids'] = form.curator.data
        session['iids'] = form.interviewer.data
        session['fids'] = form.featuring.data
        session['credits'] = form.credits.data
        session['credits_ar'] = form.credits_ar.data
        session['inst_ids'] = form.inst.data
        session['event_desc'] = form.event_desc.data
        session['event_desc_ar'] = form.event_desc_ar.data
        session['footage_desc'] = form.footage_desc.data
        session['footage_desc_ar'] = form.footage_desc_ar.data
        session['catids'] = form.categories.data
        session['topids'] = form.topics.data
        session['kids'] = form.keywords.data
        session['arch_notes'] = form.notes.data
        session['tids'] = form.title_of_edited_video.data
        #session['venue'] = form.venue.data
        form_dict={}
        form_dict['root_dir'] = form.root_dir.data
        form_dict['event_title'] = form.event_title.data
        form_dict['event_title_ar'] = form.event_title_ar.data
        form_dict['current_date'] = form.current_date.data
        form_dict['event_date'] = form.event_date.data
        form_dict['event_date_until'] = form.event_date_until.data
        form_dict['vid'] = form.videographer.data
        form_dict['ven_id'] = form.venue.data
        form_dict['cam_aud'] = form.cam_aud.data
        form_dict['aids'] = form.artists.data
        form_dict['cids'] = form.curator.data
        form_dict['iids'] = form.interviewer.data
        form_dict['fids'] = form.featuring.data
        form_dict['credits'] = form.credits.data
        form_dict['credits_ar'] = form.credits_ar.data
        form_dict['inst_ids'] = form.inst.data
        form_dict['event_desc'] = form.event_desc.data
        form_dict['event_desc_ar'] = form.event_desc_ar.data
        form_dict['footage_desc'] = form.footage_desc.data
        form_dict['footage_desc_ar'] = form.footage_desc_ar.data
        form_dict['catids'] = form.categories.data
        form_dict['topids'] = form.topics.data
        form_dict['kids'] = form.keywords.data
        form_dict['arch_notes'] = form.notes.data
        form_dict['tids'] = form.title_of_edited_video.data
        
        if Utils.verify_root_path(form_dict['root_dir']):            
            print("#########++++ONE+++++=============")
            path = Utils.create_dir(form_dict) 
            rec = {}
            written = False
            if Utils.verify_abs_path(path): 
                print("  # ++++TWO+++++=============")
                rec = Utils.write_new_rec(form_dict,path)
                print('RECCCC____ '+str(rec))
                if rec:
                    print("  # ++++THREE+++++=============")
                    written = Utils.write_to_dict(rec)
                    print("WRITTEN >>> "+str(written))
                    if written:
                        print("  # ++++FOUR+++++=============")
                        Utils.open_folder_after_creation(path)
                        flash('written successfully!')
                        ### the redirect to the same page till i make a new one....
                        return redirect(url_for('index'))
                    else:
                        flash('an error occured during writing, please attempt again...')
                        render_template('index.html', form=form)
                else:
                    flash('An ERROR occured upon creation of the record, please verify your input...')
                    render_template('index.html', form=form)
            else:
                flash('the path already exists...')
                render_template('index.html', form=form)
        else:
            flash('root directory Doesnt Exist')
            return render_template('index.html', form=form, session=session)
        #if not InputForm.create_dir(form_dict['root_dir']):
        #    flash('error on Root Directory')
        
    return render_template('index.html', form=form)


@app.route('/artist',methods=['GET'])
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
