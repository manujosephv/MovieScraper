from gmusicapi import Mobileclient
from Config import Config
from Song import Song
import difflib
from Singleton import Singleton

from Logging import Logging
logger = Logging.logger



class GoogleMusic:

    __metaclass__ = Singleton
    
    def __init__(self):
        self.gmusicapi = Mobileclient(debug_logging=False)
        logged_in = self.gmusicapi.login(email=Config.GOOGLE_MUSIC_USER_NAME, password=Config.GOOGLE_MUSIC_APP_PASSWORD, locale='en_US', android_id=Mobileclient.FROM_MAC_ADDRESS)
        if not logged_in:
            raise Exception('Unable to log in to GoogleMusic')

    def get_lib_from_gmusic(self):
        lib = self.gmusicapi.get_all_songs()
        lib_list = []
        song= None
        for song in lib:
            song = Song(artist = song['artist'], title = song['title'])
            lib_list.append(song)
        return lib_list

    def delete_playlist_if_exists(self,name):
        all_playlists=self.gmusicapi.get_all_playlists()
        for playlist in all_playlists:
            if playlist['name'] == name:
                self.gmusicapi.delete_playlist(playlist['id'])

    def create_playlist(self,name, description, public=True):
        return self.gmusicapi.create_playlist(name=name, description=description, public=public)

    def add_songs_to_playlist(self,playlist_id, song_ids=None, song_df=None):
        if (song_ids is None and song_df is None):
            raise ValueError('Need song_ids or song_dfs to add to playlist')
        if song_df is not None and (not song_df.empty):
            song_ids = song_df.google_music_store_id.dropna().tolist()
        return self.gmusicapi.add_songs_to_playlist(playlist_id, song_ids)

    def gmusic_constrained_search(self,song,query,strict):
        song_hits = query['song_hits']
        for result in song_hits:
            track = result['track']
            
            if song.remix:
                if "remix" not in track['title'].lower():
                    continue
            else:
                if "remix" in track['title'].lower():
                    continue
            if strict:
                full_title = "{} - {}".format(track['albumArtist'],track['title'])
                score = difflib.SequenceMatcher(None,song.full_title.lower(),full_title.lower()).ratio()
                if score < 0.6:
                    continue
            return track
        return None

    
    def search_song(self,song, strict=False):
        try:
            first_query = self.gmusicapi.search(song.full_title)
            first_result = self.gmusic_constrained_search(song,first_query,strict)
            if first_result is None:
                second_query = self.gmusicapi.search(song.full_title_stripped)
                first_result = self.gmusic_constrained_search(song,second_query,strict)
            if first_result is None:
                logger.warning('No satisfactory result found in Google Music for {}'.format(song.full_title))
            return first_result
        except Exception as e:
            logger.debug('Exception: {}'.format(e))
            logger.info(u'Skipped {}'.format(song.title))
            return None
    
    def get_store_id(self,result):
        store_id=None
        if result:
            if result.has_key('storeId'):
                store_id = result['storeId']
        return store_id
    
    def get_google_rating(self,result):
        rating = None
        if result:
            if result.has_key('rating'):
                return result['rating']
        return rating
    
    def update_playlist(self,playlist, public=True, exclude_0_rating = True):
        #Delete Playlist if present.
        logger.info(u'Updating the playlist {} in GoogleMusic'.format(playlist.name))
        self.delete_playlist_if_exists(playlist.name)
        #Create Playlist
        playlist_id=self.create_playlist(name=playlist.name, description= playlist.description, public=public)
        if exclude_0_rating:
            playlist.song_df = playlist.song_df[playlist.song_df['google_music_rating']!= '1']
        self.add_songs_to_playlist(playlist_id=playlist_id, song_df=playlist.song_df)

