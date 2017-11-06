# -*- coding: utf-8 -*-
from Spotify import Spotify
from GoogleMusic import GoogleMusic
from Pocket import PocketHelper
from Logging import Logging
logger = Logging.logger





def main(playlist_url, sort_popularity, strict=False,collect_skipped=False):
    spotify = Spotify()
    gmusic = GoogleMusic()
    playlist = spotify.get_playlist(playlist_url=playlist_url, sort_popularity= sort_popularity,
                         gmusic=gmusic,collect_skipped=collect_skipped)
    gmusic.update_playlist(playlist=playlist, public= True)

def scan_pocket():
    pocket = PocketHelper()
    pocket.scan_items(function_to_run=main, spotify=True)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a script to port a spotify playlist to Google Music.')
    parser.add_argument('-u','--url', dest='url', type=str, help='URL of the Spotify playlist to be copied.')
    parser.add_argument('-s','--sort', dest='sort', action='store_true', help='To sort in the order of the popularity of the track in Spotify.')
    ##Depracating multiple argument
#    parser.add_argument('-m,','--multiple', dest='multiple', action='store_true', help='To copy multiple Spotify Playlists by taking user input.')
    parser.add_argument('-t,','--strict', dest='strict', action='store_true', help='To specify if the Google Music matching is strict. Will skip tracks if not found.')
    parser.add_argument('-c,','--collect', dest='collect_skipped', action='store_true', help='To specify if the tracks not found in Google Music should be added to Youtube Playlist.')
    parser.add_argument('-p,','--pocket', dest='pocket', action='store_true', help='To copy Spotify Playlists saved in Pocket.')
    args = parser.parse_args()
    if args.pocket:
        scan_pocket()
    ##Deprecated
    elif args.multiple:
        input_list = []
        while True:    # infinite loop
            input_string = raw_input("Enter Spotify Playlist url(Exit to quit): ")
            if input_string.lower() == "exit":
                break  # stops the loop
            else:
                popularity_sort_flag = raw_input("Sort by Popularity? (Y/N): ")
                while popularity_sort_flag.lower() not in ['y','n']:
                    popularity_sort_flag = raw_input("Invalid Input. Sort by Popularity? (Y/N): ")
                if popularity_sort_flag.lower() == 'Y':
                    sort_flag = True
                else:
                    sort_flag = False
                input_list.append((input_string,sort_flag))
        for url, flag in input_list:
            main(url,flag)
    else:
        if args.url is None:
            parser.error('Without -m or -p flags, a Spotify Playlist URL is required. Please use -u')
        main(playlist_url=args.url,sort_popularity=args.sort,collect_skipped= args.collect_skipped, strict= args.strict)
    logger.info('**********Port process complete***********')

#scan_pocket()