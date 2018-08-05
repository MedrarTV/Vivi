# -*- coding: utf-8 -*-
import csv
import re
import os
import pandas as pd
import subprocess
import datetime
from input_form import InputForm


class Utils():

    def get_valid_filename(s):
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', s)

    def verify_root_path(root_dir):
        return os.path.isdir(root_dir)

    def verify_abs_path(abs_path,dict_dir='dictionaries/',dict_name='main_dict'):
        with open(dict_dir+dict_name+'.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file,delimiter=',')
            for i in reader:
                if i['directory'].find(abs_path) >-1:
                    return False
        return True

    def determine_cam_aud(i):
        cam_aud=''
        if i <= 3:
            cam_aud = 'C-'+str(i)
        else:
            cam_aud = 'A-'+str(i-3)
        return cam_aud

    def create_dir(form_dict,separator =';'):
        root_dir = form_dict['root_dir']
        cur_date = form_dict['current_date']
        cur_date = cur_date.strftime('%Y-%m-%d')
        event_title = Utils.get_valid_filename(form_dict['event_title'])
        ven_id = form_dict['ven_id']
        vid = form_dict['vid']
        cam_aud = form_dict['cam_aud']
        venue =''
        videographer = ''
        relative_path =''

        cam_aud = Utils.determine_cam_aud(int(cam_aud))

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
                    videographer = item['videographer']
                    break

        relative_path = cur_date[0:4]+separator+event_title+'\\'+cur_date[5:7]+separator+venue+'\\'+cur_date[8:10]+separator+videographer+'\\'+cam_aud
        abs_path = ''

        print("RELATIVE PATH >>>> " +relative_path)
        print("ABSOLUTE PATH >>>> " +abs_path)
        print("ROOT PATH >>>> " +root_dir)

        if(os.path.isdir(root_dir)):
            try:
                abs_path = os.path.join(root_dir, relative_path)
                if os.path.isdir(abs_path):
                    return "DIRECTORY ALREADY EXISTS!"
                else:
                    os.makedirs(abs_path)
                    return abs_path
            except FileExistsError as e:
                print("the Directory Already Exists",e)
                return e
        else:
            print("NO ROOT DIRECTORY")
            return "ROOT DIRECTORY DOESN\'T EXIST!"

    def clone_dict(src,dst):
        res = dst
        keys_list = list(set(src.keys()).intersection(dst.keys()))
        for i in keys_list:
            if i != 'id':
                res[i]=src[i]
        return res

    def group_dict(ids, dict_keys=['name', 'name_ar'], dict_name='people', dicts_dir='dictionaries/', separator=';'):

        dictionary = pd.read_csv(dicts_dir+dict_name+'.csv',error_bad_lines=False)
        res_dict = dict.fromkeys(dict_keys)

        for key in res_dict.keys():
            res_dict[key] = []

        if not ids or len(ids) ==0:
            return res_dict

        for i in ids:
            i = int(i) -1

            temp_dict = dict(dictionary.iloc[i])
            for j in temp_dict.keys():
                if j in dict_keys:
                    res_dict[j].append(temp_dict[j])

        for k in res_dict.keys():
            if res_dict[k]:
                res_dict[k] = separator.join(list(res_dict[k]))

        return res_dict

    def write_new_rec(form_dict, directory, keys_list=InputForm.keys_list, dicts_dir='dictionaries/', edited=0):

        max_id = (pd.read_csv(dicts_dir+'main_dict.csv').max()['id']+1).astype(int)

        main_dict = dict.fromkeys(keys_list)
        main_dict = Utils.clone_dict(form_dict, main_dict)
        main_dict['id'] = str(max_id)
        print('****************************'+main_dict['id']+'///////-----')
        main_dict['normalized_title'] = Utils.get_valid_filename(main_dict['event_title'])

        print("  # ++++WRRRRRR ONE+++++=============")

        videographer = pd.read_csv(dicts_dir+'videographers.csv')
        videographer = videographer.iloc[int(main_dict['vid'])-1]
        main_dict['vid_short'] = dict(videographer)['vid_short']
        main_dict['videographer'] = dict(videographer)['videographer']
        main_dict['videographer_ar'] = dict(videographer)['videographer_ar']

        print("  # ++++WRRRRRR TWO+++++=============")

        venue = pd.read_csv(dicts_dir+'venues.csv')
        venue = dict(venue.iloc[int(main_dict['ven_id'])-1])
        main_dict = Utils.clone_dict(venue, main_dict)

        print("  # ++++WRRRRRR THREE+++++=============")

        main_dict['cam_aud'] = Utils.determine_cam_aud(int(main_dict['cam_aud']))

        print("}}}}}}} AIDS LIST }}}}}}}}} "+str(list(main_dict['aids'])))
        print("}}}}}}} CIDS LIST }}}}}}}}} "+str(main_dict['cids']))

        artists = Utils.group_dict(list(main_dict['aids']))
        curators = Utils.group_dict(list(main_dict['cids']))
        interviewers = Utils.group_dict(list(main_dict['iids']))
        featuring = Utils.group_dict(list(main_dict['fids']))

        print("  # ++++WRRRRRR FOUR+++++=============")

        main_dict['artists'] = artists['name']
        main_dict['artists_ar'] = artists['name_ar']
        main_dict['curator'] = curators['name']
        main_dict['curator_ar'] = curators['name_ar']
        main_dict['interviewer'] = interviewers['name']
        main_dict['interviewer_ar'] = interviewers['name_ar']
        main_dict['featuring'] = featuring['name']
        main_dict['featuring_ar'] = featuring['name_ar']

        print("  # ++++WRRRRRR FIVE+++++=============")

        venues = Utils.group_dict(list(main_dict['inst_ids']),['venue','venue_ar'],'venues')

        main_dict['inst'] = venues['venue']
        main_dict['inst_ar'] = venues['venue_ar']

        main_dict['categories'] = Utils.group_dict(list(main_dict['catids']), ['category'], 'categories')['category']
        main_dict['keywords'] = Utils.group_dict(list(main_dict['kids']), ['keyword'], 'keywords')['keyword']
        main_dict['topics'] = Utils.group_dict(list(main_dict['topids']), ['topic'], 'topics')['topic']

        print("  # ++++WRRRRRR SIX+++++=============")

        edited_videos = Utils.group_dict(list(main_dict['tids']), ['title', 'title_ar', 'url'], 'title_of_edited_videos')

        main_dict['titles_of_vids'] = edited_videos['title']
        main_dict['titles_of_vids_ar'] = edited_videos['title_ar']
        main_dict['vids_url'] = edited_videos['url']

        print("  # ++++WRRRRRR SEVEN+++++=============")

        main_dict['directory'] = directory
        main_dict['edited']= edited

        return main_dict

    def write_to_dict(rec, keys_list=InputForm.keys_list, dict_name='main_dict', dicts_dir='dictionaries/'):
        print('//////////*****'+rec['id']+'****/////////////')
        with open(dicts_dir+dict_name+'.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file,keys_list)
            try:
                writer.writerow(rec)
                return True
            except IOError as e:
                print('ERROR >>>> ',e)

    def open_folder_after_creation(dir):
        try:
            subprocess.Popen('explorer '+dir)
            return True
        except Exception as e:
            print('ERROR >>>> ', e)
    
    def view_main_dict(table_keys):
        with open('dictionaries/main_dict.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')                        
            return [dict(i) for i in reader]
