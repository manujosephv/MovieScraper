from Config import Config
import pylast
from Singleton import Singleton

from Logging import Logging
logger = Logging.logger


class LastFM:
    
    __metaclass__ = Singleton

    def __init__(self):
        self.last_fm_api = pylast.LastFMNetwork(api_key=Config.LAST_FM_KEY, api_secret=Config.LAST_FM_SECRET)

    def get_album_art_last_fm(self,song):
        network = self.last_fm_api
        album = network.get_track(song.artist, song.title).get_album()
        if album:
            return album.get_cover_image(size=4)
        else:
            return None

    def get_genre_from_last_fm(self,song):
        genre = 'Unavailable'
        try:
            artist = self.last_fm_api.get_artist(song.artist)
            if artist:
                top_itms = artist.get_top_tags()
                if top_itms:
                    if len(top_itms)>0:
                        top_itm = top_itms[0]
                        tag = top_itm.item
                        if tag:
                            genre = tag.get_name()
        except pylast.WSError:
            logger.debug("Genre not found for {}".format(song.full_title))
            #Need to log the error
        return genre
