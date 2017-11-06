# -*- coding: utf-8 -*-
import billboard
from Config import Config
from Song import Song
import datetime as dt
import pandas as pd

class Billboard:
    
    
    def get_billboard_chart(self,chart_id):
        return billboard.ChartData(chart_id)
    
    def get_billboard_chart_as_list(self,chart_id, gmusic=None):
        song_list = []
        entries = self.get_billboard_chart(chart_id)
        for entry in entries:
            song = Song(artist=entry.artist,title = entry.title, 
                        billboard_rank = entry.rank, 
                        billboard_date = dt.datetime.now(),
                        billboard_change = entry.change)
            if gmusic:
                result = gmusic.search_song(song)
                song.google_music_store_id = gmusic.get_store_id(result)
                song.google_music_rating = gmusic.get_google_rating(result) 
            song_list.append(song)
        return song_list
    
    def get_concatenated_billboard_chart(self):
        #Getting the charts
        top_100_df = self.get_billboard_chart_as_df(Config.BILLBOARD_HOT_100)
        top_edm_df = self.get_billboard_chart_as_df(Config.BILLBOARD_TOP_EDM)
        top_hiphop_df = self.get_billboard_chart_as_df(Config.BILLBOARD_TOP_HIPHOP)
        #Removing Duplicates and concatenating the dfs
        edm_title_list = top_edm_df.full_title.get_values()
        top_100_title_list = top_100_df.full_title.get_values()
        mask_edm = [entry not in top_100_title_list for entry in edm_title_list]
        top_edm_df = top_edm_df[mask_edm]
        hiphop_title_list = top_hiphop_df.full_title.get_values()
        mask_hiphop = [entry not in top_100_title_list for entry in hiphop_title_list]
        top_hiphop_df = top_hiphop_df[mask_hiphop]
        hiphop_title_list_new = top_hiphop_df.full_title.get_values()
        edm_title_list_new = top_edm_df.full_title.get_values()
        mask_edm_hiphop = [entry not in edm_title_list_new for entry in hiphop_title_list_new]
        top_hiphop_df = top_hiphop_df[mask_edm_hiphop]
        concat_billboard_charts = pd.concat([top_100_df,top_edm_df,top_hiphop_df]).sort_values(by='billboard_rank')
        return concat_billboard_charts
