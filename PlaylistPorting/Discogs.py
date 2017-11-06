from Config import Config
import discogs_client
from Singleton import Singleton


class Discogs:

    __metaclass__ = Singleton
    
    def __init__(self):
        self.discogs_api = discogs_client.Client('ExampleApplication/0.1', user_token=Config.DISCOGS_KEY)

    def get_album_art_discogs(self,song):
        results = self.discogs_api.search(release_title=song.title,artist=song.artist,type='release')
        if len(results)>0:
            release = results[0]
            images = release.images
            if len(images)>0:
                return images[0]['resource_url']
        return None