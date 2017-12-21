from unidecode import unidecode
import re

class Song:

    def __init__(self,artist=None, title=None, full_title=None, video_link=None, 
    	youtube_id=None, genre =None, album=None, spotify_popularity = None, 
    	billboard_rank = None, google_music_rating = None, google_music_store_id = None,
    	billboard_date=None, billboard_change = None):
        
        if (artist is None) & (title is None):
            if full_title is None:
                raise ValueError('Need artist and title, or full_title to be entered')
            else:
                self.full_title = self.get_clean_title(full_title)
                self.artist, self.title = self.split_title(self.full_title)
#        elif (artist is None) | (title is None):
#            raise ValueError('Need artist and title, or full_title to be entered')
        else:
            self.artist = artist
            self.title = title
            self.full_title = u'{} - {}'.format(artist,title)
        if self.artist:
            self.artist_stripped = self.strip_ft_artist(self.artist)
        else:
            self.artist_stripped = None
        if self.title:
            self.title_stripped = self.strip_ft_title(self.title)
        else:
            self.title_stripped = None
        self.full_title_stripped = u'{} - {}'.format(self.artist_stripped, self.title_stripped)
        self.genre = genre
        self.album = album
        self.spotify_popularity = spotify_popularity
        self.billboard_rank = billboard_rank
        self.billboard_date = billboard_date
        self.billboard_change = billboard_change
        self.google_music_store_id = google_music_store_id
        self.google_music_rating = google_music_rating
        if youtube_id is None:
            if video_link is not None:
                if 'youtu' in video_link:
                    youtube_id = get_youtube_code_from_link(video_link)
        else:
            video_link = get_youtube_link_from_code(youtube_id)
        self.video_link = video_link
        self.youtube_id = youtube_id
        if 'remix' in self.full_title.lower():
            self.remix = True
        else:
            self.remix = False
        
    def __repr__(self):
       return self.full_title

    def split_title(self,title):
        split = re.split(r'(?: ?)-(?: ?)',title)
        if len(split)>1:
            return split[0],split[1]
        else:
            return title,title
      
    def strip_ft_artist(self,artist):
          return re.split(r'(?: *?)(?:\(|\[|\{)?(ft\.?|feat\.?|featuring\.?)',artist)[0]

    def strip_ft_title(self,title):
        match_remix = re.search(r'(.*)(?: *?)(?:\(|\[|\{)?(ft\.?|feat\.?|featuring\.?)(.*)(\(.*\))',title)
        if match_remix:
            title_without_ft = match_remix.group(1)+match_remix.group(4)
        else:
            match_ft = re.search(r'(.*)(?: +?)(?:\(|\[|\{)?(ft\.?|feat\.?|featuring\.?)(?: +?)(.*)(?:\)|\]|\})?',title)
            if match_ft:
                title_without_ft = match_ft.group(1)
            else:
                title_without_ft = title
        return title_without_ft


    def get_clean_title(self, full_title):
        #Removing | from title if any
        if "|" in full_title:
          full_title = full_title.replace('|','')

        words_filter = ('official', 'lyric video', 'official video','official music video','lyrics','official lyric video','official lyrics video','lyric', 'audio', 'remixed', 'video',
                'full', 'version', 'music', 'mp3', 'hd', 'hq', 'uploaded', 'reupload','re-upload','proximity release','edm.com exclusive','edm.com premeire'
                ,'free download!','free download','visualizer','official audio')
        word_filter_calc = ["("+word+")" for word in words_filter] + ["["+word+"]" for word in words_filter] + ["{"+word+"}" for word in words_filter] 
        match = re.search(r'(.*)((\(|\[|\{).*(\)|\]|\}))',full_title)
        if match:
            song_name_words = match.group(1).split()+[match.group(2)]
    #         print("regex match found")
        else:
            song_name_words = full_title.split()
    #         print('normal split:{}'.format(len(song_name_words)))
        result_words = [word for word in song_name_words if word.lower() not in word_filter_calc]
        result = ' '.join(result_words)
        # result.decode('unicode_escape').encode('ascii','ignore')
        return unidecode(result)


    def to_dict(self):
        return {
            'artist':self.artist,
            'title': self.title,
            'full_title' : self.full_title,
            'artist_stripped': self.artist_stripped,
            'title_stripped':self.title_stripped,
            'full_title_stripped': self.full_title_stripped,
            'genre':self.genre,
            'album':self.album,
            'spotify_popularity': self.spotify_popularity,
            'billboard_rank': self.billboard_rank,
            'billboard_date':self.billboard_date,
            'billboard_change' : self.billboard_change,
            'google_music_store_id' : self.google_music_store_id,
            'google_music_rating': self.google_music_rating,
            'video_link': self.video_link,
            'youtube_id': self.youtube_id
        }



#### Static
def get_youtube_code_from_link(link):
    tag = re.search(r'(https|http)://\w+.youtube.\w+/watch\?v=(.{11})', link)
    if tag:
        return tag.group(2)
    else:
        tag = re.search(r'(https|http)://youtu\.be/(.{11})', link)
        if tag:
            return tag.group(2)
        else:
            return None
#### Static
def get_youtube_link_from_code(code):
    return "http://www.youtube.com/watch?v={}".format(code)

