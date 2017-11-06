# -*- coding: utf-8 -*-
from Config import Config
from pocket import Pocket, PocketException
from Singleton import Singleton
from Logging import Logging
logger = Logging.logger


class PocketHelper:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        self.p = Pocket(consumer_key=Config.POCKET_CONSUMER_KEY,access_token=Config.POCKET_ACCESS_TOKEN)
        
    def run_spotify(self,item,url,function_to_run):
        if 'spotify' in url.lower():
            logger.info(u'Getting url for {} from Pocket'.format(item['resolved_title']))
            flag = False
            strict = False
            collect_skipped = False
            if 'tags' in item:
                if 'sort' in item['tags']:
                    flag = True
                if 'strict' in item['tags']:
                    strict = True
                if 'collect' in item['tags']:
                    collect_skipped = True
            logger.info('url: {}, flag: {}'.format(url,flag))
            function_to_run(url,flag,strict, collect_skipped)
    
    def run_youtube(self,item,url,function_to_run):
        if 'youtube' in url.lower():
            logger.info(u'Getting url for {} from Pocket'.format(item['resolved_title']))
            limit = None
            strict = False
            collect_skipped = False
            if 'tags' in item:
                if any(key.startswith('recent') for key in item['tags']):
                    for key in item['tags'].keys():
                        if key.startswith('recent'):
                            limit = int(key.split('recent')[-1])
                        if key.startswith('strict'):
                            strict = True
                        if key.startswith('collect'):
                            collect_skipped = True
                        
            logger.debug('url: {}, limit: {}, strict: {}'.format(url,limit, strict))
            function_to_run(url,limit,strict, collect_skipped)
        

    
    def scan_items(self,function_to_run, youtube=False, spotify=False):
        if (youtube is None) and (spotify is None):
            raise ValueError('Either Youtube flag or Spotify Flag should be given')
        logger.info('Scanning Pocket........')
        items=self.p.retrieve(state='unread', detailType='complete')
        for key in items['list'].keys():
            item = items['list'][key]
            url = item['given_url']
            if spotify:
                self.run_spotify(function_to_run=function_to_run, item=item, url=url)
            if youtube:
                self.run_youtube(function_to_run=function_to_run, item=item, url=url)
        logger.info('Scanning Pocket completed')
            # p.archive(key)
        # p.commit()