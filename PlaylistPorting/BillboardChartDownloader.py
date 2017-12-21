from Config import Config
from MusicTools import MusicTools
import codecs
from iTunes import iTunes
from Billboard import Billboard
import pandas as pd


from Logging import Logging
logger = Logging.logger

MAX_SONG_DOWNLOAD = Config.BILLBOARD_MAX_SONG_DOWNLOAD

def get_chart_songs_to_download():
    logger.info('Getting charts from Billboard')
    billboard = Billboard()
    billboard_chart_df = billboard.get_concatenated_billboard_chart()
    logger.debug('Billboard chart length: {}'.format(len(billboard_chart_df.index)))
    logger.info('Checking for new songs from last download'.format(len(billboard_chart_df.index)))
    last_download_chart = pd.read_pickle(Config.BILLBOARD_LAST_DOWNLOAD)
    billboard_chart_df.to_pickle(Config.BILLBOARD_LAST_DOWNLOAD)
    mt = MusicTools()
    billboard_chart_df['old_matched_title'] = billboard_chart_df['full_title_stripped'].apply(lambda x: mt.closest_match(x,last_download_chart.full_title_stripped.values))
    billboard_chart_df = billboard_chart_df[billboard_chart_df['old_matched_title']=='No Match'].reset_index(drop=True)
    logger.info('Getting songs from iTunes library')
    itunes = iTunes()
    itunes_lib = itunes.get_itunes_lib_as_df()
    logger.debug('Itunes Lib length: {}'.format(len(itunes_lib.index)))
    logger.info('Finding out songs which are already in the library')
    billboard_chart_df['matched_title'] = billboard_chart_df['full_title_stripped'].apply(lambda x: mt.closest_match(x,itunes_lib.full_title_stripped.values))
    songs_not_in_lib = billboard_chart_df[billboard_chart_df['matched_title']=='No Match'].reset_index(drop=True)
    logger.debug('songs not in lib length: {}'.format(len(songs_not_in_lib.index)))
    global MAX_SONG_DOWNLOAD
    if MAX_SONG_DOWNLOAD < len(songs_not_in_lib.index):
        MAX_SONG_DOWNLOAD = len(songs_not_in_lib.index)+1
    return songs_not_in_lib.loc[:MAX_SONG_DOWNLOAD-1,:]



def main(max_song_download=Config.BILLBOARD_MAX_SONG_DOWNLOAD):
    global MAX_SONG_DOWNLOAD
    MAX_SONG_DOWNLOAD = max_song_download
    open(Config.BILLBOARD_DOWNLOAD_FAILED_FILE_NAME, 'w').close()
    song_list = get_chart_songs_to_download()
    if len(song_list.index)>0:
        mt = MusicTools()
        logger.info('Downloading {} songs...'.format(len(song_list)))
        for index, row in song_list.iterrows():
            song = mt.get_song_from_title(row['full_title'])
            if song:
                # pass
                logger.info(u"Song- title: {}".format(row['full_title']))
                status = mt.download_music(song.video_link, row['full_title'], is_quiet=True)
                # status = 1
                if status == 0:
                            mt.fix_id3(song)
                else:
                    logger.error(u"Downloading of {} failed. Moving to the next item...".format(row['full_title']))
                    with codecs.open(Config.BILLBOARD_DOWNLOAD_FAILED_FILE_NAME,encoding='utf-8', mode='a+') as f:
                        f.write("{}\n".format(row['full_title']))
            else:
                logger.error(u"No results found for {}. Moving to the next item...".format(row['full_title']))
                with codecs.open(Config.BILLBOARD_DOWNLOAD_FAILED_FILE_NAME,encoding='utf-8', mode='a+') as f:
                    f.write(u"{}\n".format(row['full_title']))
        logger.info('*************************Billboard Chart Download Finished***************************')
    else:
        logger.error("No Songs to be downloaded. Quiting...")
    


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a script to download the top songs from the Billboard Charts')
    parser.add_argument('-l','--limit', type=int,help='This specified the top x number of songs to be downloaded. If left blank, top 25 songs are downloaded.', required=False, default = 25)
    args = parser.parse_args()
    main(args.limit)
#    main(3)