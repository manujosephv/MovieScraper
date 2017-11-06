import os
import json


class Config:

    ### LOADING THE CONFIG VARIABLES FROM FILE
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except:
        with open('../config.json', 'r') as f:
            config = json.load(f)
    GOOGLE_MUSIC_APP_PASSWORD = config['GOOGLEMUSIC']['APP_PASSWORD']
    GOOGLE_MUSIC_USER_NAME = config['GOOGLEMUSIC']['USER_NAME']
    GOOGLE_MUSIC_DUMP_FILE_NAME = os.path.join(config['DEFAULT']['ROOT'],config['GOOGLEMUSIC']['DUMP_FILE_NAME']) 
    GOOGLE_MUSIC_LAST_READ_FILE_NAME = os.path.join(config['DEFAULT']['ROOT'],config['GOOGLEMUSIC']['LAST_READ_FILE_NAME'])
    GOOGLE_MUSIC_DOWNLOAD_FAILED_FILE_NAME = os.path.join(config['DEFAULT']['ROOT'],config['GOOGLEMUSIC']['DOWNLOAD_FAILED_FILE_NAME'])
    GOOGLE_DEVELOPER_KEY = config['MUSICTOOLS']['GOOGLE_DEVELOPER_KEY'] #My Key - Manage by going to https://console.cloud.google.com
    YOUTUBE_API_SERVICE_NAME = config['MUSICTOOLS']['YOUTUBE_API_SERVICE_NAME']
    YOUTUBE_API_VERSION = config['MUSICTOOLS']['YOUTUBE_API_VERSION']
    YOUTUBE_TO_WATCH_PLAYLIST = config['MUSICTOOLS']['YOUTUBE_TO_WATCH_PLAYLIST']
    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret.
    CLIENT_SECRETS_FILE = config['MUSICTOOLS']['CLIENT_SECRETS_FILE']
    # This OAuth 2.0 access scope allows for full read/write access to the
    # authenticated user's account and requires requests to use an SSL connection.
    YOUTUBE_SCOPES = config['MUSICTOOLS']['YOUTUBE_SCOPES']
    GOOGLE_CUSTOM_SEARCH_API_SERVICE_NAME = config['MUSICTOOLS']['CUSTOM_SEARCH_API_SERVICE_NAME']
    GOOGLE_CUSTOM_SEARCH_API_VERSION = config['MUSICTOOLS']['CUSTOM_SEARCH_API_VERSION']
    GOOGLE_ALBUM_ART_SEARCH_ID = config['MUSICTOOLS']['ALBUM_ART_SEARCH_ID']
    DOWNLOAD_PATH = config['MUSICTOOLS']['DOWNLOAD_PATH']
    LAST_FM_KEY = config['MUSICTOOLS']['LAST_FM_KEY']
    LAST_FM_SECRET = config['MUSICTOOLS']['LAST_FM_SECRET']
    DISCOGS_KEY = config['MUSICTOOLS']['DISCOGS_KEY']
    ITUNES_PATH = config['MUSICTOOLS']['ITUNES_PATH']
    BACKUP_PATH = config['DEFAULT']['ROOT']
    TODOIST_PROJECT_NAME = config['TODOIST']['PROJECT_NAME']
    TODOIST_API_KEY = config['TODOIST']['TODOIST_API_KEY']
    TODOIST_YOUTUBE_COLLECT_PROJECT = config['TODOIST']['YOUTUBE_COLLECT_PROJECT']
    BILLBOARD_HOT_100 = config['BILLBOARD']['HOT_100']
    BILLBOARD_TOP_HIPHOP = config['BILLBOARD']['TOP_HIPHOP']
    BILLBOARD_TOP_EDM = config['BILLBOARD']['TOP_EDM']
    BILLBOARD_DOWNLOAD_FAILED_FILE_NAME = os.path.join(config['DEFAULT']['ROOT'],config['BILLBOARD']['DOWNLOAD_FAILED_FILE_NAME']) 
    BILLBOARD_LAST_DOWNLOAD = os.path.join(config['DEFAULT']['ROOT'],config['BILLBOARD']['LAST_DOWNLOAD']) 
    BILLBOARD_MAX_SONG_DOWNLOAD = config['BILLBOARD']['MAX_SONGS']
    SPOTIPY_CLIENT_ID = config['SPOTIFY']['SPOTIPY_CLIENT_ID']
    SPOTIPY_CLIENT_SECRET = config['SPOTIFY']['SPOTIPY_CLIENT_SECRET']
    POCKET_CONSUMER_KEY = config['POCKET']['POCKET_CONSUMER_KEY']
    POCKET_ACCESS_TOKEN = config['POCKET']['POCKET_ACCESS_TOKEN']




