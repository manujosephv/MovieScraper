from Config import Config
from libpytunes import Library
from Song import Song
import os
import shutil
import pandas as pd

from Logging import Logging
logger = Logging.logger

class iTunes:

	def backup_file(self,file_path, backup_path):
	    logger.info('Copying iTunes xml to working directory')
	    path, file_name = os.path.split(file_path)
	    backup_full_path = os.path.join(backup_path,file_name)
	    #Copy
	    shutil.copy(file_path,backup_full_path)
	    return backup_full_path


	def get_itunes_lib(self):
	    path = self.backup_file(Config.ITUNES_PATH, Config.BACKUP_PATH)
	    l = Library(path)
	    songs = l.songs.items()
	    song_list = []
	    for id, song in songs:
	        song_model = None
	        song_model = Song(artist=song.artist, title = song.name, genre=song.genre, album=song.album)
	        song_list.append(song_model)
	    return song_list

	def get_itunes_lib_as_df(self):
		song_list = self.get_itunes_lib()
		return pd.DataFrame([s.to_dict() for s in song_list])
