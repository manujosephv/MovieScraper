from Config import Config
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import difflib
import re
from Playlist import Playlist
from Singleton import Singleton
import datetime as dt
import logging
#from urlparse import urlparse, parse_qs
from Song import Song, get_youtube_link_from_code
import HTMLParser
import urlparse
from Logging import Logging
logger = Logging.logger
#logger.setLevel(logging.WARNING)

def global_imports(modulename,shortname = None, asfunction = False):
    if shortname is None: 
        shortname = modulename
    if asfunction is False:
        globals()[shortname] = __import__(modulename)
    else:        
        globals()[shortname] = eval(modulename + "." + shortname)

class Youtube:

    # Set GOOGLE_DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
    # tab of
    #   https://cloud.google.com/console
    # Please ensure that you have enabled the YouTube Data API for your project.
    
    __metaclass__ = Singleton
    
    def __init__(self,secure = False):
        if secure:
            # When running locally, disable OAuthlib's HTTPs verification. When
            # running in production *do not* leave this option enabled.
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
            flow = InstalledAppFlow.from_client_secrets_file(Config.CLIENT_SECRETS_FILE, Config.YOUTUBE_SCOPES)
            credentials = flow.run_console()
            self.youtube = build(Config.YOUTUBE_API_SERVICE_NAME, Config.YOUTUBE_API_VERSION, credentials = credentials,cache_discovery=False)
        else:
            credentials = None
            self.youtube = build(Config.YOUTUBE_API_SERVICE_NAME, Config.YOUTUBE_API_VERSION, developerKey=Config.GOOGLE_DEVELOPER_KEY, cache_discovery=False)
        
        self.html_parser = HTMLParser.HTMLParser()
        self.to_watch_playlist = None


    def youtube_search(self,query,max_results):
        #To get the audio and not the video
        query = query + ' audio'
        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = self.youtube.search().list(
          q=query,
          part="id,snippet",
          maxResults=max_results
        ).execute()

        songs = []
        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get("items", []):
          if search_result["id"]["kind"] == "youtube#video":
            song = None
            song = Song(full_title=search_result["snippet"]["title"], youtube_id = search_result["id"]["videoId"] )
            songs.append(song)
        return songs

    def get_youtube_video(self,full_title):
        #Searching in Youtube
        search_result = self.youtube_search(full_title,1)
        if len(search_result)>0:
          song = search_result[0]
          score = difflib.SequenceMatcher(None,song.full_title.lower(),full_title.lower()).ratio()
          if score < 0.50:
              logger.warning(u"Youtube Title: {}, Actual Title: {}, Score: {}. No satisfactory results in Youtube".format(song.full_title,full_title,score))
              return None
        else:
          logger.warning(u"No Results for {} in Youtube".format(full_title))
          return None
        return song

    def extract_youtube_link_from_text(self,item):
        match = re.search(r'(?:https|http):\/\/(?:www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9-_]{11}', item)
        if match:
            return match.group()
        else:
            match = re.search(r'(?:https|http):\/\/youtu\.be\/[a-zA-Z0-9-_]{11}', item) 
            if match:
              return match.group()
            else: 
              return None
#        u_pars = urlparse(item)
#        quer_v = parse_qs(u_pars.query).get('v')
#        if quer_v:
#            return quer_v[0]
#        pth = u_pars.path.split(' ')[0].split('/')
#        if pth:
#            return get_youtube_link_from_code(pth[-1])
#        
    
    def get_title_from_youtube_code(self,vid_code):
        # Call the videos.list method to retrieve results matching the specified
        # video code.
        search_response = self.youtube.videos().list(
        part='snippet',
            id=vid_code,
        ).execute()
        return search_response['items'][0]['snippet']['title']
    
    def get_upload_playlist_id_from_username_channel(self,username=None, channel_id = None):
        if (username is None) & (channel_id is None):
            raise ValueError('Either Channel id or username needs to be there')
        channels_response = self.youtube.channels().list(
            part='contentDetails',
          forUsername=username,
          id = channel_id
        ).execute()
        try:
            playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        except Exception as e:
            logger.debug(e)
            playlist_id = None
        return playlist_id
    
    def get_channel_title(self, channel_id):
        channels_response = self.youtube.channels().list(
            part='snippet',
          id = channel_id
        ).execute()
        return channels_response['items'][0]['snippet']['title']
    
    def get_song_list_from_playlist_id(self,playlist_id, gmusic=None, limit=None, strict = False, collect_skipped=False):
        # Retrieve the list of videos uploaded to the authenticated user's channel.
        MAX_SONGS_PER_QUERY = 50
        playlistitems_list_request = self.youtube.playlistItems().list(
            playlistId=playlist_id,
            part="snippet",
            maxResults=MAX_SONGS_PER_QUERY
            )
        song_list = []
        counter = 0
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()
            # Print information about each video.
            for playlist_item in playlistitems_list_response["items"]:
                full_title = playlist_item["snippet"]["title"]
                video_id = playlist_item["snippet"]["resourceId"]["videoId"]
                song = Song(full_title=full_title,video_link = get_youtube_link_from_code(video_id))
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
                            if song.youtube_id:
                                if self.to_watch_playlist is None:
                                    self.to_watch_playlist = self.get_playlist('https://www.youtube.com/playlist?list={}'.format(Config.YOUTUBE_TO_WATCH_PLAYLIST))
                                existing_ids=self.to_watch_playlist.song_df.youtube_id.values
                                if song.youtube_id not in existing_ids:
                                    ToDoist.ToDoist().add_item(item=song.video_link,project_name=Config.TODOIST_YOUTUBE_COLLECT_PROJECT)
#                                    self.add_video_to_playlist(video_id = song.youtube_id, playlist_id=Config.YOUTUBE_TO_WATCH_PLAYLIST)
                    song.google_music_store_id=gmusic.get_store_id(first_result)
                    song.google_music_rating = gmusic.get_google_rating(first_result)
                    if song.google_music_store_id:
                        counter = counter+1
                song_list.append(song)
                
                if limit:
                    if counter>int(limit):
                        return song_list
            playlistitems_list_request = self.youtube.playlistItems().list_next(
            playlistitems_list_request, playlistitems_list_response)
        return song_list
    
    def get_playlist_name_description(self,playlist_id):
        result = self.youtube.playlists().list(
            part="snippet",
            id=playlist_id
          ).execute()
        title = None
        description = None
        if 'items' in result.keys():
            items = result['items']
            if len(items)>0:
                snippet = items[0]['snippet']
                if 'title' in snippet.keys():
                    title = self.html_parser.unescape(snippet['title'])
                if 'description' in snippet.keys():
                    description = self.html_parser.unescape(snippet['description'])
        return title, description
    
    def get_playlist_id_name_description(self,url):
        url_data = urlparse.urlparse(url)
        query = urlparse.parse_qs(url_data.query)
        username = None
        channel = None
        if query.has_key('list'):
            playlist_id = query['list'][0]
            
        else:
            if 'user' in url_data.path:
                username = url_data.path.split('/')[-1]
#                playlist_name = username
#                playlist_desc = 'The song uploads from {}.'.format(playlist_name)
            elif 'channel' in url_data.path:
                channel = url_data.path.split('/')[-1]
#                playlist_name = self.get_channel_title(channel)
#                playlist_desc = 'The song uploads from {}.'.format(playlist_name)
            playlist_id = self.get_upload_playlist_id_from_username_channel(username=username, channel_id=channel)
        
        playlist_name, playlist_desc = self.get_playlist_name_description(playlist_id)
        if playlist_name:
            if 'Uploads from' in playlist_name:
                playlist_name = playlist_name.split('Uploads from ')[-1]
        if channel or username:
            playlist_desc = 'The song uploads from {} as on {}.'.format(playlist_name, dt.datetime.today().strftime('%d-%b-%y'))
        return playlist_name, playlist_desc, playlist_id
            
    
    
    def get_playlist(self,playlist_url,gmusic=None, limit=None, strict = False, collect_skipped=False):
        if collect_skipped:
            global_imports('ToDoist')
        playlist_name, playlist_desc, playlist_id = self.get_playlist_id_name_description(playlist_url)
        if limit:
            playlist_name = '{} {}'.format(playlist_name, limit)
        logger.info(u'Getting playlist {} from Youtube'.format(playlist_name))
        if playlist_id:
            song_list = self.get_song_list_from_playlist_id(playlist_id,gmusic,limit, strict, collect_skipped) 
            if collect_skipped:
                ToDoist.ToDoist().api.commit()
            return Playlist(name=playlist_name, description=playlist_desc, song_list=song_list)
        
    def add_video_to_playlist(self,video_id,playlist_id):
        self.youtube.playlistItems().insert(
        part="snippet",
        body = {'snippet': {'playlistId': playlist_id,
  'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}}
        ).execute()
        
        

    
    
    
    
    