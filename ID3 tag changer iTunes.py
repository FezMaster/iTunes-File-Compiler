#-*- coding: utf-8 -*-
from mutagen.mp3 import MP3, EasyMP3
from mutagen.easyid3 import EasyID3
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER, APIC
from mutagen import MutagenError
import glob 
import shutil
import os
from urllib.parse import unquote
import plistlib

OldLocs = glob.glob(r"C:\Users\FezMaster\Music\iTunes\iTunes Media\Music\**\*.mp3", recursive = True)#Change this file address to whereever your iTunes music library is located.
dst = r"C:\Users\FezMaster\Music\iTunes\ID3 Tag Edits Destination Folder\ "#Change this to the address of your destination folder.
dst = dst[:-1]
samenamecount = {}
filescopied = 0

data=plistlib.load(open(r"C:\Users\FezMaster\Music\Library.plist", "rb"))#Change this to wherever you've saved your exported iTunes library. Make sure it's a plist file, not xml.
tracks=list(map(lambda a: a[1], data['Tracks'].items()))#List of dictionaries containing song data

def getSongInfo(path):
    for track in tracks:
        if(unquote(track['Location'].replace("file://localhost/", "")).replace("/", "\\").lower() == path.lower()):
            return track

for element in OldLocs:
    LibList = getSongInfo(element)#This section copies and renames the mp3 files
    if LibList is None:#This detects mp3 files in the source directory that are not entered in the iTunes library.
        print (element)
    src = element
    newfilename = LibList['Name']
    for char in newfilename:#Can't have these characters in a Windows file name.
        if char in '?/"*':
            newfilename = newfilename.replace(char, '')
    while os.path.exists(dst + newfilename + '.mp3'):#This prevents file overwriting.
        if LibList['Name'] not in samenamecount:
            samenamecount[LibList['Name']] = 0
        samenamecount[LibList['Name']] += 1
        newfilename = newfilename + ' - ' + str(samenamecount[LibList['Name']])
    dstnew = dst + newfilename + ".mp3"
    shutil.copy(src, dstnew)
    
    mp3tags = MP3(dstnew, ID3 = EasyID3)#This section changes the ID3 tags
    mp3tags['title'] = [LibList['Name']]
    try:
        if 'Artist' in LibList:#Some of my songs have no Artist name entered, which would give a Key Error, hence the if.
            mp3tags['artist'] = [LibList['Artist']]
    except MutagenError:
        print ("Error with track " + LibList['Name'])
    mp3tags.save(v2_version=3)
    filescopied += 1#This is just a little progress meter essentially. Prints a message every 100 songs.
    if (filescopied % 100) == 0:
        print (str(filescopied) + " files copied")

#The code below will change the album art as well, which is why I don't want to delete it. May come in handy later.

# filez = glob.glob(r"C:\Users\Owen\Music\iTunes\iTunes Media\Music\100 gecs\**\*.mp3", recursive = True)
# dst = r"C:\Users\Owen\Music\iTunes\ID3 Tag Edits Destination Folder\ "
# dst = dst[:-1]

# for element in filez: #This section copies the mp3 files to another location, renaming the copied files in the process.
    # src = element
    # newfilename = element
    # newfilename = newfilename[78:]
    # x = newfilename.find("(")
    # if x != -1: 
        # newfilename = newfilename[:(x - 1)]
    # newfilename = newfilename.replace("_", " ")
    # dstnew = dst + newfilename + ".mp3"
    # shutil.copy(src, dstnew)
    
    # mp3tags = MP3(dstnew, ID3 = EasyID3)#This section changes the album title
    # mp3tags['album'] = ['bruh sound effect pack vol. 1']
    # mp3tags.save(v2_version=3)
    
    # albumart = open(rb'C:\Users\Owen\Pictures\billdab4.png', 'rb')#This section changes the album art
    # mp3tags = EasyMP3(dstnew, ID3=ID3)
    # mp3tags.tags.delall("APIC")
    # mp3tags.save(v2_version=3)
    # mp3tags.tags.add(
        # APIC(
            # encoding=3,
            # mime=u'image/jpeg',
            # type=3,
            # desc=u'gec tree',
            # data=albumart.read()
            # )
        # )
    # mp3tags.save(v2_version=3)
