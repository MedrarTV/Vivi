# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, jsonify, request, Response, flash
from flask_bootstrap import Bootstrap
from input_form import InputForm
import json
import os
from add_items import ArtistForm, VenueForm, ShooterForm, ItemForm
from table_crud import ArchiveItems
from utilities import Utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vtrardem'
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = 'G:\\work and courses\\Medrar\\uploading_testing\\'

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
    form = InputForm()
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
    form = ArtistForm()
    if form.validate_on_submit():
        print('i am here')
        name=form.name.data
        name_ar = form.name_ar.data
        categories = form.categories.data
        biography = form.biography.data
        biography_ar = form.biography_ar.data
        website = form.website.data
        ArtistForm.create_artist(name,name_ar,categories,biography,biography_ar,website)
        return redirect(url_for('index'))
    return render_template('add_artist.html', form=form)


@app.route('/add_videographer', methods=['GET','POST'])
def add_videographer():
    form = ShooterForm()
    if form.validate_on_submit():
        shortname = form.shooter_short.data
        name = form.shooter_name.data
        name_ar = form.shooter_name_ar.data
        ShooterForm.create_shooter(shortname,name,name_ar)
        return redirect(url_for('index'))
    return render_template('add_videographer.html', form=form)


@app.route('/add_venue', methods=['GET','POST'])
def add_venue():
    form = VenueForm()
    if form.validate_on_submit():        
        shortname = form.venue_short.data
        venue = form.venue.data
        venue_ar = form.venue_ar.data
        desc = form.description.data
        desc_ar = form.description_ar.data
        website = form.website.data
        VenueForm.create_venue(shortname,venue,venue_ar,desc,desc_ar,website)
        return redirect(url_for('index'))
    return render_template('add_venue.html', form=form)

@app.route('/table_view', methods=['GET'])
def table_view():
    table_dict = Utils.view_main_dict(ArchiveItems.table_keys)
    #print(table_dict)
    table_view = ArchiveItems(table_dict)
    table_view.border = True
    return render_template('items_table.html',table=table_view)


@app.route('/edit_item/<id>', methods=['GET', 'POST'])
def edit_item(id):
    return str(ArchiveItems.get_row(int(id)-1))

@app.route('/clone_item/<id>', methods=['GET', 'POST'])
def clone_item(id):
    row =ArchiveItems.get_row(int(id)-1)
    print(row['root_dir'])
    form = InputForm()
    #form = form.populate_obj(row)
    form.data = row
    return render_template('index.html', form=form)

@app.route('/search', methods=['GET','POST'])
def search():
    return "Search page is comming soon!"

@app.route('/add_category',methods=['GET','POST'])
def add_category():
    if request.method == "POST":
        print("add category accessed...")
        category_item = request.json
        ItemForm.create_single_item(category_item, 'categories')
        print(category_item)
        return redirect(url_for('index'))

@app.route('/add_keyword',methods=['POST'])
def add_keyword():
    if request.method == "POST":
        print("add keyword accessed...")
        keyword_item = request.json
        ItemForm.create_single_item(keyword_item,'keywords')
        print(keyword_item)
        return redirect(url_for('index'))

@app.route('/add_topic',methods=['GET','POST'])
def add_topic():
    if request.method == "POST":
        print("add topic accessed...")
        topic_item = request.json
        ItemForm.create_single_item(topic_item, 'topics')
        print(topic_item)
        return redirect(url_for('index'))


@app.route('/add_event_type', methods=['GET', 'POST'])
def add_event_type():
    return 'add event type'




if __name__ == '__main__':
    app.run()
