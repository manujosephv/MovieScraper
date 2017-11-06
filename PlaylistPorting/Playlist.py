# -*- coding: utf-8 -*-
import pandas as pd

class Playlist:

    def __init__(self,name=None, description=None, song_df=None, 
                 song_list=None, spotify_popularity_sort=False):
        
        if (song_df is None) & (song_list is None):
            raise ValueError('Need song_df or song_list to create object')
        self.name= name
        self.description= description
        self.spotify_popularity_sort = spotify_popularity_sort
        if song_list:
            self.song_list = song_list
            self.song_df = self.get_song_df(song_list)
        else:
            self.song_df = song_df
            
    def get_song_df(self,song_list):
        song_df = pd.DataFrame([s.to_dict() for s in song_list])
        if self.spotify_popularity_sort:
            song_df.sort_values('spotify_popularity', ascending = False, inplace=True)
        return song_df
            


