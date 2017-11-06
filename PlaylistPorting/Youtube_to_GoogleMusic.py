# -*- coding: utf-8 -*-
from Youtube import Youtube
from GoogleMusic import GoogleMusic
from Pocket import PocketHelper
from Logging import Logging
logger = Logging.logger





def main(playlist_url, limit=None, strict = False, collect_skipped = False):
    if 'youtube' in playlist_url:
        youtube = Youtube(secure=False)
        gmusic = GoogleMusic()
        playlist = youtube.get_playlist(playlist_url=playlist_url,
                             gmusic=gmusic, limit=limit, strict = strict, collect_skipped = collect_skipped)
        gmusic.update_playlist(playlist=playlist, public= True)

def scan_pocket():
    pocket = PocketHelper()
    pocket.scan_items(function_to_run=main, youtube = True)


import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a script to port a Youtube playlist to Google Music.')
    parser.add_argument('-u','--url', dest='url', type=str, help='URL of the Youtube playlist to be copied.')
    parser.add_argument('-l','--limit', dest='limit', type=int, help='To limit the playlist to a few most recent items.')
    ##Deprecated multiple option
#    parser.add_argument('-m,','--multiple', dest='multiple', action='store_true', help='To copy multiple Youtube Playlists by taking user input.')
    parser.add_argument('-t,','--strict', dest='strict', action='store_true', help='To specify if the Google Music matching is strict. Will skip tracks if not found.')
    parser.add_argument('-c,','--collect', dest='collect_skipped', action='store_true', help='To specify if the tracks not found in Google Music should be added to Youtube Playlist.')
    parser.add_argument('-p,','--pocket', dest='pocket', action='store_true', help='To copy Youtube Playlists saved in Pocket.')
    args = parser.parse_args()
    if args.pocket:
        scan_pocket()
    ##Deprecated
    elif args.multiple:
        input_list = []
        while True:    # infinite loop
            input_string = raw_input("Enter Youtube Playlist url(Exit to quit): ")
            if input_string.lower() == "exit":
                break  # stops the loop
            else:
                limit = raw_input("Most recent x songs in the playlist: ")
                input_list.append((input_string,limit))
        for url, limit in input_list:
            main(url,limit)
    else:
        if args.url is None:
            parser.error('Without -m or -p flags, a Youtube Playlist URL is required. Please use -u')
        main(playlist_url=args.url,limit=args.limit,strict=args.strict, collect_skipped=args.collect_skipped)
    logger.info('**********Port process complete***********')
    
#main('https://www.youtube.com/watch?v=k2qgadSvNyU&list=PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG', limit=25, strict=True, collect_skipped=True)
#scan_pocket()