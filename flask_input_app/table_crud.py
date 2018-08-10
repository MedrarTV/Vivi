from flask_table import Table, Col, LinkCol
import utilities
import pandas as pd
from datetime import datetime

class ArchiveItems(Table):
    id = Col('Id', show=False)
    event_title = Col('Event Title')
    event_title_ar = Col('عنوان الحدث')
    current_date = Col('Shooting Date')
    videographer = Col('Shooter')
    videographer_ar = Col('المصور')
    venue = Col('Location')
    venue_ar = Col('المكان')
    cam_aud = Col('Cam/Aud')
    arch_notes = Col('Notes')
    directory = Col('Path')
    #edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    clone = LinkCol('Clone', 'clone_item', url_kwargs=dict(id='id'))
    
    table_keys=['id', 'event_title', 'event_title_ar', 'current_date', 'event_date', 'vid_short', 
                'videographer', 'videographer_ar', 'ven_short', 'venue', 'venue_ar', 'cam_aud', 'arch_notes', 
                'directory']
            
class ItemObject():
    root_dir ='' 
    event_title = ''
    event_title_ar = ''
    current_date = ''
    event_date = ''
    event_date_until = ''
    videographer = []
    venue = []
    artists = []
    credits = ''
    credits_ar = ''
    curator = []
    inst = []
    event_desc = ''
    event_desc_ar = ''
    footage_desc = ''
    footage_desc_ar = ''
    categories = []
    notes = ''
    interviewer = []
    featuring = []
    title_of_edited_video = []
    keywords = []
    topics = []
    cam_aud = []
