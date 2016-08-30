# -*- coding: utf-8 -*-
'''
    medrar.py - pandora_client plugin

    custom parse_path for pandora_client to parse medrar archive paths in the form

    Festival/Artist Name/Work Name/MVI_2036.MOV

'''
import sys

import csv
import re
import ox
import unicodedata
'''
    This is a medrar specific function, to be used in other context in their tool set 
'''
def Normalize (str):
    ''' Comment out what you don't need'''

    # changed slahs into a unicode value that looks similar
    str=re.sub("/","∕",str)
    # remove extra spaces
    str=re.sub(r"\s+", " ",str).strip()
    # remove spaces around semiclons
    str= re.sub (r'\s*;\s*', ';',str)
    # remove spaces in the beginning and end
    str= re.sub ('^\s*|\s*$', '',str)
    # remove newlines in the beginning and end
    str= re.sub ('^\r*\n*|\n*\r*$', '',str,re.M)
    #u" ".join(str.encode('utf-8')).strip()

    return str


def example_path(client):
    return '\t' + 'Festival/Artist Name/Work Name/MVI_2036.MOV'

def parse_path(client, path, prefix):
    '''
        args:
            client - Client instance
            path   - path without volume prefix 
        return:
            return None if file is ignored, dict with parsed item information otherwise
    '''
    m = re.compile('^(?P<project>.+?)/(?P<artist>.+?)/(?P<workname>.+?)/.*').match(path)
    #print m
    #print path
    if not m:
        return None
    #print "we are in pattern"
    info = m.groupdict()
    ex = re.compile('.*exclude.*')
    if ex.match(path):
        return None
    match = 0
    summary =''
    year = ''
    artists = []
    #By=u""
    #print prefix
    ''' Attempt to read data from a CSV file, residing inside "project" path; and has the same name as the project
        with a .csv extension.

        This process tries to capture:
           * Multiple Artists
           * Collective Name
           * Artist Pseudo Name
           * Production Year
           * Synopsis
    '''
    try:
        with open(u""+prefix+"/"+info['project']+"/"+info['project']+".csv",'rb') as f:
            festivalCSV=csv.reader(f, delimiter=',')
            rd = csv.DictReader(f)
            #By=u""
            selection = []
            for dictRow in rd:
                #By=u""
                #artists = []
                try:
                    #WorkName_Normalized=re.sub(' +',' ',(re.sub("/","∕",dictRow['Title']).strip()))
                    WorkName_Normalized=Normalize(dictRow['Title'])
                    CollectiveOrPseudo=Normalize(dictRow['Collective/Pseudo'])
                    FirstArtist=Normalize(dictRow['First Name']+" "+dictRow['Last Name'])
                    OtherArtists=Normalize(dictRow['Other'])
    
                    if CollectiveOrPseudo:
                        By=CollectiveOrPseudo
                    elif OtherArtists:
                        By=Normalize(FirstArtist+";"+OtherArtists)
                    elif FirstArtist:
                        By=FirstArtist
                    else:
                        By="N/A"
                except KeyError:
                    print "Key Error in sheet"
    
    
                try:
                    #if  By == info['artist'].encode("utf-8"):
                    #    print "found artist match "+By
                    #if WorkName_Normalized == info['workname'].encode("utf-8"):
                    #    print "found Workname match "+WorkName_Normalized
                    #    print "current artist is "+By+" and info is "+info['artist']
                    if  By == info['artist'].encode("utf-8") and WorkName_Normalized == info['workname'].encode("utf-8"):
                            #print "Match found for "+info['artist'].encode('utf-8')+' '+info['workname'].encode('utf-8')
                            match = 1
    
                            #create a list of artists
                            artists= [artist for artist in [Normalize(dictRow['Collective/Pseudo']),FirstArtist]+OtherArtists.split(';') if artist and not isinstance(artist,list) and not artist == "\n"]
    
                            #if one artist and Collective/Pseudo provided, or only Collective/Pseudo provided, then consider it a pseudo name
                            if len(artists) <= 1:
                                ArtistPseudo=CollectiveOrPseudo
                            #if multiple artists and Collective/Pseudo provided, then consider it a collective name
                            else:
                                Collective=CollectiveOrPseudo
    
                            #read teh rest of the fields
                            year= dictRow['Year of production']
                            summary = dictRow['Synopsis']
                            #What is the status of ths works (Festivale Specific):
                            # ["not accepted", "initial acception", "screened", "re-screened"]
                            if not dictRow['Yes/No'] and not dictRow['PRE-SELECTION']:
                                selection= ["N/A"]
                            else:
                                if re.match("(Yes|Y|1|yes|y)",dictRow['Yes/No']) is not None :
                                    selection= ["screened"]
                                elif re.match("(?iYes|Y|1)",dictRow['PRE-SELECTION']) is not None :
                                    selection= ["initial acception"]
                                elif re.match("(?iNo|N|0)",dictRow['PRE-SELECTION']) is not None :
                                    selection= ["not accepted"]
                                else:
                                    selection= ["ERR"]
                            #if len(artists) == 2 and dictRow['Collective/Pseudo']:
                                #print "pseudo :"+  dictRow['Collective/Pseudo']
                                #print artists
                            #elif len(artists) > 2 and dictRow['Collective/Pseudo']:
                                #print "Collective:" + dictRow['Collective/Pseudo']
                                #print artists
                            #print artists
                            break
                except UnicodeDecodeError:
                    print dictRow
                    print "UnicodeDecodeError on "
        if match == 0:
            print "No match found for "+info['artist'].encode('utf-8')+' '+info['workname'].encode('utf-8')
            #print str(path)
    except OSError:
        print "No csv file found!!"
    #No information found in sheet; just take it from filesystem
    if match == 0:
        print "No match found for "+info['artist'].encode('utf-8')+' '+info['workname'].encode('utf-8')
        By = Normalize(info['artist'])
        artists = By.split(";")
        WorkName_Normalized = Normalize(info['workname'])

    #title = "%s by %s" % (unicodedata.normalize('NFC',info['workname']), By)
    #print ArtistName_Normalized
    #print unicodedata.normalize('NFD',ArtistName_Normalized.decode('utf-8'))
    #print WorkName_Normalized
    #print WorkName_Normalized.decode('utf-8')
    #print unicodedata.normalize('NFD',WorkName_Normalized.decode('utf-8'))
    #print By
    #print By.decode('utf-8')
    #By = u" ".join(By).strip()
    #By = unicodedata.normalize('NFD',u" ".join(By.decode('utf-8')).strip())
    r = {
        'artist': artists,
        'project': [info['project']],
        'title': "%s by %s" % (WorkName_Normalized, By),
        'summary': summary,
        'date': year,
        'selection': selection,
    } 
    #print info['project']
    _info = ox.movie.parse_path(path)
    for key in ('extension', 'type'):
        r[key] = _info[key]
    return r

def ignore_file(client, path):
    '''
        return True if file should not even be considered.
        i.e. to filter out .DS_Store, empty files
    '''
    filename = os.path.basename(path)
    if filename.startswith('._') \
        or filename in ('.DS_Store', ) \
        or filename.endswith('~') \
        or not os.path.exists(path) \
        or os.stat(path).st_size == 0:
        return True
    return False
