# -*- coding: utf-8 -*-

from GoogleMusic import GoogleMusic
from Billboard import Billboard
from Config import Config
from Playlist import Playlist
import datetime as dt
import pandas as pd

from Logging import Logging
logger = Logging.logger


charts_to_playlist = [('HOT_100',"Billboard Hot 100 Chart"),('TOP_HIPHOP', 'Billboard R&B and HipHop Chart'),('TOP_EDM', 'Billboard EDM Chart')] #

def current_week(day):
    day_of_week = day.weekday()

    to_beginning_of_week = dt.timedelta(days=day_of_week)
    beginning_of_week = day - to_beginning_of_week

    return beginning_of_week.strftime('%d-%b-%y')


def main():
    logger.info('Scanning the Billboard Charts......')
    chart_df_dict = {}
    gmusic = GoogleMusic()
    billboard = Billboard()
    for chart,chart_name in charts_to_playlist:
        logger.info('Getting {}......'.format(chart_name))
        chart_list = billboard.get_billboard_chart_as_list(chart_id=Config.config['BILLBOARD'][chart], gmusic=gmusic)
        playlist=Playlist(name=chart_name, description= chart_name+' from Billboard on week {}'.format(current_week(dt.datetime.today())),
                          song_list= chart_list)
        
        logger.info('Updating {} Playlist......'.format(chart_name))
        
        gmusic.update_playlist(playlist, public=True)
        chart_df_dict[chart] = playlist.song_df
    
    #Top Rising from Hot 100
    if chart_df_dict.has_key('HOT_100'):
        logger.info('Updating {} Playlist......'.format('Top 25 Risers'))
        top_100=chart_df_dict['HOT_100']
        top_100.loc[top_100.billboard_change=='Hot Shot Debut','billboard_change'] = 100
        top_100.change = pd.to_numeric(top_100.billboard_change, errors='coerce').fillna(0)
        hot25_risers=top_100.sort_values(by=['billboard_change'], ascending=False).head(25).sort_values(by=['billboard_rank'], ascending=True)
        playlist = Playlist(name='Top 25 Risers', 
                            description='Top 25 Risers from Hot 100 Billboard on week {}'.format(current_week(dt.datetime.today())),
                            song_df=hot25_risers)
        gmusic.update_playlist(playlist=playlist, public= True)
        logger.info('Finished Updating......'.format('Top 25 Risers'))


import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This is a script to update the playlists in Google Music with latest Billboard Charts')
    args = parser.parse_args()
    main()

