from flask_table import Table, Col, LinkCol
import utilities
import pandas as pd
from werkzeug import MultiDict


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
    #clone = LinkCol('Clone', 'clone', url_kwargs=dict(id='id'))
    
    table_keys=['id', 'event_title', 'event_title_ar', 'current_date', 'event_date', 'vid_short', 
                'videographer', 'videographer_ar', 'ven_short', 'venue', 'venue_ar', 'cam_aud', 'arch_notes', 
                'directory']
    
    def get_row(id):
        row = pd.read_csv('dictionaries/main_dict.csv').iloc[id-1]
        return pd.Series.to_dict(row)
        #return MultiDict(pd.Series.to_dict(row))
            
