# -*- coding: utf-8 -*-
from Config import Config
from pocket import Pocket, PocketException
from Youtube import Youtube
from GoogleMusic import GoogleMusic
from Spotify import Spotify
from Singleton import Singleton
from Logging import Logging
logger = Logging.logger


class PocketHelper:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        self.p = Pocket(consumer_key=Config.POCKET_CONSUMER_KEY,access_token=Config.POCKET_ACCESS_TOKEN)
        
    def run_spotify(self,item,url,function_to_run, key):
        if 'spotify' in url.lower():
            logger.info(u'Getting url for {} from Pocket'.format(item['resolved_title']))
            flag = False
            strict = False
            collect_skipped = False
            delete = False
            if 'tags' in item:
                if 'sort' in item['tags']:
                    flag = True
                if 'strict' in item['tags']:
                    strict = True
                if 'collect' in item['tags']:
                    collect_skipped = True
                if 'delete' in item['tags']:
                    delete = True
            logger.info('url: {}, sort: {}, strict: {}, collect: {}, delete: {}'.format(url,flag, strict, collect_skipped, delete))
            if delete:
                self.delete_playlist_mark_read(playlist_url=url,key=key)
            else:
                function_to_run(url,flag,strict, collect_skipped)
    
    def run_youtube(self,item,url,function_to_run, key):
        if 'youtube' in url.lower():
            logger.info(u'Getting url for {} from Pocket'.format(item['resolved_title']))
            limit = None
            strict = False
            collect_skipped = False
            delete = False
            if 'tags' in item:
                if any(key.startswith('recent') for key in item['tags']):
                    for key in item['tags'].keys():
                        if key.startswith('recent'):
                            limit = int(key.split('recent')[-1])
                        if key.startswith('strict'):
                            strict = True
                        if key.startswith('collect'):
                            collect_skipped = True
                        if key.startswith('delete'):
                            delete = True
                        
            logger.debug('url: {}, limit: {}, strict: {}, collect: {}, delete: {}'.format(url,limit, strict, collect_skipped, delete))
            if delete:
                self.delete_playlist_mark_read(playlist_url=url,limit=limit,key=key)
            else:
                function_to_run(url,limit,strict, collect_skipped)
    
    def delete_playlist_mark_read(self, playlist_url,key,limit=None):
        if 'youtube' in playlist_url:
            youtube=Youtube()
            playlist_name, playlist_desc, playlist_id = youtube.get_playlist_id_name_description(playlist_url, limit)
        elif 'spotify' in playlist_url:
            spotify = Spotify()
            playlist_name, playlist_desc, tracks = spotify.get_playlist_name_desc_tracks(playlist_url)
        gmusic = GoogleMusic()    
        gmusic.delete_playlist_if_exists(playlist_name)
        self.p.archive(key)
        self.p.commit()

    def scan_items(self,function_to_run, youtube=False, spotify=False):
        if (youtube is None) and (spotify is None):
            raise ValueError('Either Youtube flag or Spotify Flag should be given')
        logger.info('Scanning Pocket........')
        items=self.p.retrieve(state='unread', detailType='complete')
        for key in items['list'].keys():
            item = items['list'][key]
            url = item['given_url']
            if spotify:
                self.run_spotify(function_to_run=function_to_run, item=item, url=url, key=key)
            if youtube:
                self.run_youtube(function_to_run=function_to_run, item=item, url=url,key=key)
        logger.info('Scanning Pocket completed')
            # p.archive(key)
        # p.commit()
        
