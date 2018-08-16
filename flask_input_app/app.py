# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, redirect, url_for, jsonify, request, Response, flash
from flask_bootstrap import Bootstrap
from input_form import InputForm
import json
import os
from add_items import ArtistForm, VenueForm, ShooterForm, ItemForm
from table_crud import ArchiveItems, ItemObject
from utilities import Utils
import pandas as pd
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vtrardem'
app.config['DEBUG'] = True

bootstrap = Bootstrap(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index(itemObj = None):
    if itemObj:
        form = InputForm(obj=itemObj)
        form.populate_obj(itemObj)       
    else:        
        last_record_id = Utils.get_max_id()-1
        last_root_dir = pd.read_csv('dictionaries/main_dict.csv').iloc[last_record_id]['root_dir']
        if Utils.verify_root_path(last_root_dir):
            itemObj=ItemObject()
            itemObj.root_dir = last_root_dir
            form = InputForm(obj=itemObj)
            form.populate_obj(itemObj)            
        else:
            form = InputForm()

    if form.validate_on_submit():        
        form_dict={}
        form_dict['root_dir'] = form.root_dir.data
        form_dict['event_title'] = form.event_title.data
        form_dict['event_title_ar'] = form.event_title_ar.data
        form_dict['current_date'] = form.current_date.data
        form_dict['unkn_date'] = form.unkn_date.data
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
            path = Utils.create_dir(form_dict)
            if path is not False:
                rec = {}
                written = False
                if Utils.verify_abs_path(path['relative_path']):                
                    rec = Utils.write_new_rec(form_dict,path['relative_path'])                
                    if rec:                    
                        written = Utils.write_to_dict(rec)                    
                        if written:                        
                            Utils.open_folder_after_creation(path['abs_path'])
                            flash('RECORD WRITTEN SUCCESSFULLY!!!')                        
                            return redirect(url_for('table_view'))
                        else:
                            flash('An ERROR Occured During Writing, Please Delete TThe Record and Try again...')                        
                    else:
                        flash('An ERROR occured During The Creation of The Record, Please Verify Your Input...')                 
                else:
                    flash('The Path Already Exists in The Main Dictionary.')
            else:
                flash('The Files Path Already Exists on The Computer.')              
        else:
            flash('Root Directory Doesn\'t Exist.')
            
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

@app.route('/add_video', methods=['GET','POST'])
def add_video():
    return "it will be added soon!"

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
    table_view = ArchiveItems(table_dict)
    table_view.border = True
    return render_template('items_table.html',table=table_view)


@app.route('/clone_item/<id>', methods=['GET', 'POST'])
def clone_item(id):
    record_tobe_cloned = Utils.get_record_by_id(id)
    item = Utils.populate_itemObject(record_tobe_cloned)
    return  index(item)    


@app.route('/edit_item/<id>', methods=['GET', 'POST'])
def edit_item(id):
    record_tobe_edited = Utils.get_record_by_id(id)
    item = Utils.populate_itemObject(record_tobe_edited)
    edit_form = InputForm(obj=item)
    edit_form.populate_obj(item)

    if edit_form.validate_on_submit():
        edit_form_dict = {}
        edit_form_dict['root_dir'] = edit_form.root_dir.data
        edit_form_dict['event_title'] = edit_form.event_title.data
        edit_form_dict['event_title_ar'] = edit_form.event_title_ar.data
        edit_form_dict['current_date'] = edit_form.current_date.data
        edit_form_dict['unkn_date'] = edit_form.unkn_date.data
        edit_form_dict['event_date'] = edit_form.event_date.data
        edit_form_dict['event_date_until'] = edit_form.event_date_until.data
        edit_form_dict['vid'] = edit_form.videographer.data
        edit_form_dict['ven_id'] = edit_form.venue.data
        edit_form_dict['cam_aud'] = edit_form.cam_aud.data
        edit_form_dict['aids'] = edit_form.artists.data
        edit_form_dict['cids'] = edit_form.curator.data
        edit_form_dict['iids'] = edit_form.interviewer.data
        edit_form_dict['fids'] = edit_form.featuring.data
        edit_form_dict['credits'] = edit_form.credits.data
        edit_form_dict['credits_ar'] = edit_form.credits_ar.data
        edit_form_dict['inst_ids'] = edit_form.inst.data
        edit_form_dict['event_desc'] = edit_form.event_desc.data
        edit_form_dict['event_desc_ar'] = edit_form.event_desc_ar.data
        edit_form_dict['footage_desc'] = edit_form.footage_desc.data
        edit_form_dict['footage_desc_ar'] = edit_form.footage_desc_ar.data
        edit_form_dict['catids'] = edit_form.categories.data
        edit_form_dict['topids'] = edit_form.topics.data
        edit_form_dict['kids'] = edit_form.keywords.data
        edit_form_dict['arch_notes'] = edit_form.notes.data
        edit_form_dict['tids'] = edit_form.title_of_edited_video.data

        print(str(edit_form_dict))
    return render_template('edit_record.html', form=edit_form)


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


if __name__ == '__main__':
    app.run()
