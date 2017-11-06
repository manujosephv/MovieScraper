from Config import Config
from todoist.api import TodoistAPI
from MusicTools import MusicTools
from Youtube import Youtube
from Soundcloud import Soundcloud
from Song import Song, get_youtube_code_from_link
from Singleton import Singleton

from Logging import Logging
logger = Logging.logger

class ToDoist:
    
    __metaclass__ = Singleton
    
    def __init__(self):
        self.api = TodoistAPI(Config.TODOIST_API_KEY)
        self.api.sync()
        self.mt = MusicTools()

    def find_project_id_by_name(self,project_name):
        projects = self.api.state['projects']
        for project in projects:
            if project['name'] == project_name:
                return project['id']
            
    def add_item(self, item, project_id=None, project_name = None):
        if (project_id is None) and (project_name is None):
            raise ValueError('Either project_id or project_name should be provided')
        if project_id is None:
            project_id = self.find_project_id_by_name(project_name)
        self.api.items.add(item,project_id)

    def walk_items_in_project(self, function_to_call, project=Config.TODOIST_PROJECT_NAME, commit=True, mark_read = True):
        items = self.api.state['items']
        logger.info("Scanning and Downloading ToDoist List:{}".format(project))
        for item in items:
            logger.debug(u"Scanning {}|{}".format(item['content'], item['id']))
            if item and ('checked' in item.data.keys()):
                if ((item['project_id'] == self.find_project_id_by_name(project)) & (item['checked']==0)): #For Debug  & (item['id']==112286022)    
                    function_to_call(item, mark_read)
        if commit:
            self.api.commit()

    def download_song(self,item, mark_read):
        result = 1
        song = self.get_song(item['content'])
        if song:
            logger.info(u"Scanned Results: {}|{}".format(song.full_title, song.video_link))
            result = self.mt.download_music(song.video_link, song.full_title, is_quiet=True)
            # result = 1
            logger.debug("Download Result: {} | 1 is a failure, 0 is a success".format(result))
        #1 is a failure, 0 is a success
            if result == 0:
                logger.info("Download Success. Marking item as completed...")
                if mark_read:
                    item.complete()
                self.mt.fix_id3(song)
            else:
                logger.error(u"Downloading of {} failed. Moving to the next item...".format(song.full_title))

    def get_song(self,item):
        #Checking Youtube Links
        youtube=Youtube()
        link = youtube.extract_youtube_link_from_text(item)
        if link:
            full_title = youtube.get_title_from_youtube_code(get_youtube_code_from_link(link))
            song = Song(full_title= full_title, video_link = link, )
        else:
            soundcloud = Soundcloud()
            link = soundcloud.extract_soundcloud_link_from_text(item)
            if link:
                song= Song(full_title=soundcloud.get_title_soundcloud(link), video_link = link)
            else:
                #Items without a link
                songs = youtube.youtube_search(item,1)
                if len(songs) >0 :
                    song = songs[0]
                else:
                    return None
        return song
