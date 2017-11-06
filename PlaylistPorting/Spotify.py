# -*- coding: utf-8 -*-
from Config import Config
from Song import Song
from Youtube import Youtube
from Playlist import Playlist
from Singleton import Singleton
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import HTMLParser
import re

from Logging import Logging
logger = Logging.logger

def global_imports(modulename,shortname = None, asfunction = False):
    if shortname is None: 
        shortname = modulename
    if asfunction is False:
        globals()[shortname] = __import__(modulename)
    else:        
        globals()[shortname] = eval(modulename + "." + shortname)


class Spotify:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(client_id=Config.SPOTIPY_CLIENT_ID, client_secret=Config.SPOTIPY_CLIENT_SECRET)
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        self.html_parser = HTMLParser.HTMLParser()
        
    def get_playlist_id_username_from_link(self,playlist_url):
        match = re.search(r'(https|http)://.+/user/(.+)/playlist/(.+)',playlist_url)
        username = None
        playlist_id = None
        if match:
            username = match.group(2)
            playlist_id = match.group(3)
            logger.debug(u'username: {}, playlist id: {}'.format(username, playlist_id))
        return playlist_id, username
    
    def get_song_list(self,tracks, gmusic=None, strict=False, collect_skipped=False):
        song_list = []
        for tracks in tracks['items']:
            track = tracks['track']
            artist = self.html_parser.unescape(track['artists'][0]['name'])
            title = self.html_parser.unescape(track['name'])
            popularity = track['popularity']
            song = Song(artist=artist, title=title, spotify_popularity=popularity)
            if gmusic:
                first_result = None
                try:
                    first_result = gmusic.search_song(song, strict)
                    if first_result is None:
                            raise ValueError('No result from Google Music')
                except Exception as e:
                    logger.debug('Exception: {}'.format(e))
                    logger.info(u'Skipped {}. Added to to Watch Playlist'.format(song.full_title))
                    if collect_skipped:
                        youtube = Youtube(secure=False)
                        if song.youtube_id is None:
                            youtube_video=youtube.get_youtube_video(full_title=song.full_title)
                            if youtube_video:
                                song.youtube_id = youtube_video.youtube_id
                                song.video_link = "http://www.youtube.com/watch?v={}".format(youtube_video.youtube_id)
                        if song.youtube_id:
                            if youtube.to_watch_playlist is None:
                                youtube.to_watch_playlist = youtube.get_playlist('https://www.youtube.com/playlist?list={}'.format(Config.YOUTUBE_TO_WATCH_PLAYLIST))
                            existing_ids=youtube.to_watch_playlist.song_df.youtube_id.values
                            if song.youtube_id not in existing_ids:
                                ToDoist.ToDoist().add_item(item=song.video_link,project_name=Config.TODOIST_YOUTUBE_COLLECT_PROJECT)
                song.google_music_store_id=gmusic.get_store_id(first_result)
                song.google_music_rating = gmusic.get_google_rating(first_result)
            song_list.append(song)
        return song_list
    
    def get_all_tracks_as_list(self, tracks, gmusic, strict,collect_skipped):
        logger.info('Scanning page 1')
        i=2
        song_list=self.get_song_list(tracks, gmusic, strict,collect_skipped)
        while tracks['next']:
            tracks = self.sp.next(tracks)
            logger.info('Scanning page {}'.format(i))
            i=i+1
            song_list = song_list + self.get_song_list(tracks,gmusic, strict,collect_skipped)
        return song_list
    
    def get_playlist_name_desc_tracks(self,playlist_url):
        playlist_id, username = self.get_playlist_id_username_from_link(playlist_url)
        results = self.sp.user_playlist(username, playlist_id, fields="name,description,tracks,next")
        playlist_name = self.html_parser.unescape(results['name'])
        if results.has_key('description') and results['description'] is not None:
            playlist_desc = self.html_parser.unescape(results['description'])
        else:
            playlist_desc = playlist_name
        return playlist_name, playlist_desc, results['tracks']
            
            
    def get_playlist(self,playlist_url, sort_popularity=False, gmusic=None, strict = False,collect_skipped=False):
        if collect_skipped:
            global_imports('ToDoist')
#        playlist_id, username = self.get_playlist_id_username_from_link(playlist_url)
#        results = self.sp.user_playlist(username, playlist_id, fields="name,description,tracks,next")
#        playlist_name = self.html_parser.unescape(results['name'])
#        if results.has_key('description') and results['description'] is not None:
#            playlist_desc = self.html_parser.unescape(results['description'])
#        else:
#            playlist_desc = playlist_name
        playlist_name, playlist_desc, tracks = self.get_playlist_name_desc_tracks(playlist_url)
        logger.info(u'Copying {} from Spotify to Google Music'.format(playlist_name))
        logger.debug(u'Playlist Name: {}, Playlist Description: {}'.format(playlist_name, playlist_desc))
#        tracks = results['tracks']
        song_list = self.get_all_tracks_as_list(tracks,gmusic, strict,collect_skipped)
        if collect_skipped:
                ToDoist.ToDoist().api.commit()
        return Playlist(name=playlist_name, description=playlist_desc, song_list=song_list,
                        spotify_popularity_sort = sort_popularity)
            
    