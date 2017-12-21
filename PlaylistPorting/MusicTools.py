#!/usr/bin/python
import traceback
import eyed3
import re
import os
import youtube_dl
import difflib
import requests
from PyLyrics import PyLyrics
from LastFM import LastFM
from Discogs import Discogs
from GoogleSearch import GoogleSearch
from Youtube import Youtube
from Soundcloud import Soundcloud
from Config import Config
# Version compatiblity
import sys
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import quote_plus as qp
    raw_input = input
else:
    from urllib2 import urlopen
    from urllib import quote_plus as qp

from Logging import Logging

logger = Logging.logger

class MusicTools:

  def get_album_art(self,song):
    try:
      last_fm = LastFM()
      link = last_fm.get_album_art_last_fm(song)
      if link:
        return link
    except Exception as e:
      logger.debug(e)
      # traceback.print_exc()
      pass
    logger.debug("Error in getting AlbumArt from Last.FM. Trying Discogs")
    
    try:
      discogs = Discogs()
      link = discogs.get_album_art_discogs(song)
      if link:
        return link
    except Exception as e:
      logger.debug(e)
      # traceback.print_exc()
      pass
    logger.debug("Error in getting AlbumArt from Discogs. Trying Google")
    
    try:
      google_search = GoogleSearch()
      link = google_search.get_album_art_google(song.artist +' - ' + song.title)
      if link:
        return link
    except Exception as e:
      logger.debug(e)
      traceback.print_exc()
      pass
    logger.debug("Error in getting AlbumArt from Google. Skipping..")
    return None


  def get_song_from_title(self,full_title):
      youtube = Youtube()
      song = youtube.get_youtube_video(full_title)
      if not(song):
          logger.info('No Match in Youtube. Searching Soundcloud')
          soundcloud = Soundcloud()
          song = soundcloud.get_soundcloud_song(full_title)
      return song

  def download_music(self, video_link, title, is_quiet=False):
    # logger.info('Disabled download for testing')
    # return 1
    download_source = None
    if "youtu" in video_link:
      download_source = 'YouTube'
    elif "soundcloud" in video_link:
      download_source = "Soundcloud"
    r = 1
    if download_source is not None:
        logger.info(u'Downloading {} from {}...'.format(title, download_source))
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
              }],
        'outtmpl': u'/'+ Config.DOWNLOAD_PATH +'/'+title+'.%(ext)s' ,
        # 'outtmpl': u''+ os.path.join(config['DEFAULT']['ROOT'],config['MUSICTOOLS']['DOWNLOAD_PATH'],title+'.%(ext)s') ,
        'quiet':is_quiet,
        # 'outtmpl': '/music/%(title)s.%(ext)s' ,
          }
        try:  
          with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            r = ydl.download([video_link])
        except Exception: #youtube_dl.utils.DownloadError
          r = 1
      # logger.error(e.message+" Moving on to the next item...")
    #1 is a failure, 0 is a success
    return r

  def get_closest_path(self,full_title):
    files = os.listdir(os.path.join(os.getcwd(), Config.DOWNLOAD_PATH))
    closest_file = difflib.get_close_matches(full_title+'.mp3',files)[0]
    return os.path.join(os.getcwd(), Config.DOWNLOAD_PATH, closest_file)

  def open_id3_tag(self, full_title):
    full_path = os.path.join(os.getcwd(), Config.DOWNLOAD_PATH, full_title+'.mp3')
    logger.debug(u'MP3 file path for loading is: {}'.format(full_path))
    if os.path.exists(full_path):
      try:
        audiofile = eyed3.load(full_path)
      except UnicodeEncodeError:
        audiofile = eyed3.load(self.get_closest_path(full_title))
    else:
      audiofile = eyed3.load(self.get_closest_path(full_title))
    return audiofile

  def fix_id3(self,song):
    logger.debug(u'Writing ID3 tags to {}...'.format(song.full_title))
    try:
        audiofile = self.open_id3_tag(song.full_title)
        if audiofile.tag is None:
          audiofile.tag = eyed3.id3.Tag()
    ## Getting Lyrics from LyricsWikia
        try:
          logger.debug(u'Getting Lyrics for {} from LyricsWikia'.format(song.full_title))
          lyrics = PyLyrics.getLyrics(song.artist,song.title)
          audiofile.tag.lyrics.set(u''+lyrics)
        except ValueError as e:
            logger.warning(e.message)                 

        logger.debug(u"Writing these to tags: artist:{}, Track name: {}, Album Name: {}".format(song.artist,song.title,song.album))
        artist=song.artist.strip()
        track_name=song.title.strip()
        if song.album:
            album_name=song.album.strip()
        else:
            album_name = ""
        # print (artist,track_name,album_name)

        audiofile.tag.artist=unicode(artist)
        audiofile.tag.album_artist=unicode(artist)
        audiofile.tag.title=unicode(track_name)
        audiofile.tag.album =unicode(album_name)

        last_fm = LastFM()
        genre = last_fm.get_genre_from_last_fm(song)
        if genre:
          audiofile.tag.genre =unicode(genre)
        else:
          logger.warning('Genre not found for {}'.format(song.full_title))

        try:
            logger.debug("Getting AlbumArt from Discogs/LastFM/Google...")
            image_link = self.get_album_art(song)
            imagedata = requests.get(image_link).content
            audiofile.tag.images.set(0,imagedata,"image/jpeg",u"Album Art")
        except Exception as e:
            logger.error("Error in getting AlbumArt. Won't be saved to Tag")
            logger.debug(e)
        
        audiofile.tag.save()
        logger.info(u'ID3 Tags written and saved to {}...'.format(song.full_title))

    except IOError:
        logger.error(u"Can't open file. ID3 tags skipped:{}".format(song.full_title))
    except Exception as e:
        logger.exception("Something awful has happened")
        logger.debug(e)


  def closest_match(self,title,lib_full_title_list):
    match= difflib.get_close_matches(title,lib_full_title_list, cutoff=0.8)
    #     print match
    if match:
        if len(match)>0:
            return match[0]
    else:
        return "No Match"
