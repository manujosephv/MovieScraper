from Config import Config
from apiclient.discovery import build
from Singleton import Singleton

class GoogleSearch:

    # Set GOOGLE_DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
    # tab of
    #   https://cloud.google.com/console
    # Please ensure that you have enabled the YouTube Data API for your project.
    __metaclass__ = Singleton

    def __init__(self):
        self.custom_search = build(Config.GOOGLE_CUSTOM_SEARCH_API_SERVICE_NAME, Config.GOOGLE_CUSTOM_SEARCH_API_VERSION,
               developerKey=Config.GOOGLE_DEVELOPER_KEY, cache_discovery=False)

    def get_album_art_google(self,query):
        # To skip Google Search while testing.
        # print (1/0)
        search_response= self.custom_search.cse().list(
        q=query,
        cx=Config.GOOGLE_ALBUM_ART_SEARCH_ID,
        searchType='image',
        imgType = 'photo',
        num=10,
        safe= 'off'
        ).execute()
        for item in search_response['items']:
          if item['image']['height'] == item['image']['width']:
            return item['link']
        return search_response['items'][0]['link']
