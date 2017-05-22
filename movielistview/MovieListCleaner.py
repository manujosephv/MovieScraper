# coding: utf-8

# ### Cleaning the scraped list

import pandas as pd
import re
import difflib



class MovieListCleaner:
    
    inputMovieList = pd.DataFrame()
    cleanMovieList = pd.DataFrame()
    # minRating = 6.0
    # minVotes = 1000
    std_list_of_releases = ['CAMRip','CAM','TS','TELESYNC','PDVD','WP','WORKPRINT','TC','TELECINE',
                            'PPV','PPVRip ','SCR','SCREENER','DVDSCR','DVDSCREENER','BDSCR','DDC','R5',
                            'R5.LINE','R5.AC3.5.1.HQ','DVDRip','DVDR','DVD-Full','Full-Rip','ISO rip',
                            'untouched rip','DSR','DSRip','SATRip','DTHRip','DVBRip','HDTV','PDTV','TVRip',
                            'HDTVRip','VODRip','VODR','WEBDL','WEB DL','WEB-DL','HDRip','WEBRip (P2P)',
                            'WEB Rip (P2P)','WEB-Rip (P2P)','WEB (Scene)','WEB-Cap','WEBCAP','WEB Cap',
                            'BDRip','BRRip','Blu-Ray','BluRay','BLURAY','BDMV','BDR']

    rank_list_of_releases = {'CAMRip':55 ,'CAM':54,'TS':53,'TELESYNC':52,'PDVD':51,'WP':50,'WORKPRINT':49,'TC':48,'TELECINE':47,
                            'PPV':46,'PPVRip':45,'SCR':44,'SCREENER':43,'DVDSCR':42,'DVDSCREENER':41,'BDSCR':40,'DDC':39,'R5':38,
                            'R5.LINE':37,'R5.AC3.5.1.HQ':36,'DVDRip':35,'DVDR':34,'DVD-Full':33,'Full-Rip':32,'ISO rip':31,
                            'untouched rip':30,'DSR':29,'DSRip':28,'SATRip':27,'DTHRip':26,'DVBRip':25,'HDTV':24,'PDTV':23,'TVRip':22,
                            'HDTVRip':21,'VODRip':20,'VODR':19,'WEBDL':18,'WEB DL':17,'WEB-DL':16,'HDRip':15,'WEBRip (P2P)':14,
                            'WEB Rip (P2P)':13,'WEB-Rip (P2P)':12,'WEB (Scene)':11,'WEB-Cap':10,'WEBCAP':9,'WEB Cap':8,
                            'BDRip':7,'BRRip':6,'Blu-Ray':5,'BluRay':4,'BLURAY':3,'BDMV':2,'BDR':1}

    avoid_list_of_releases = ['CAMRip','CAM','TS','TELESYNC','PDVD','WP','WORKPRINT','TC','TELECINE',
                            'PPV','PPVRip ','SCR','SCREENER','DVDSCR','DVDSCREENER','BDSCR ','DDC','R5',
                            'R5.LINE','R5.AC3.5.1.HQ']


    #def __init__(self,df, rating, votes):
    def __init__(self,df):
        self.inputMovieList = df
        #self.minRating = rating
        #self.minVotes = votes


    # ### Extracting Movie Name and other details from the file name   
    def movie_name(self,row):
        n=""
        resolution = ""
        year = 0
        match_found = False
        res_bool = False
        #debug
        #print(row)
        if row is not None:
            for part in row.split("."):
                matchObj = re.match('^(19|20)\d{2}$',part)
                if res_bool:
                    resolution = part
                    res_bool = False
                if matchObj:
                    year = matchObj.group()
                    match_found = True
                    res_bool = True
                if not match_found:
                    n = n + part +" "
                    continue
        return pd.Series({'Name':n,'Year':year,'Resolution':resolution})

# ### Extracting IMDB Rating
    
    def imdb_rating(self,row):
        print("imdb rating: {}".format(row))
        #from IPython.core.debugger import Tracer; Tracer()() 
        row = str(row).decode('unicode_escape').encode('ascii','ignore')
        if row is not None:
            row = row.replace(",","").replace("(","").replace(")","")
            match = re.search(r'\s*(\d+\.\d+)/(\d+)\s*\w+\s*(\d+)\s*\w+', row)
            if match:
                rating = match.group(1)
                votes = match.group(3)
                return pd.Series({'IMDB':rating, 'Votes':votes})
            match = re.search(r'\s*(\d+\.\d+)/(\d+)\s*', row)
            if match:
                rating = match.group(1)
                votes = 0
                return pd.Series({'IMDB':rating, 'Votes':votes})
            match = re.search(r'\s*(\w+)\s*(\d+)\s*(\w+)', row)
            if match:
                rating = 0
                votes = 0
                return pd.Series({'IMDB':rating, 'Votes':votes})
            else:
                rating = 0
                votes = 0
                return pd.Series({'IMDB':rating, 'Votes':votes})

    # ### RottenTomato Ratings
    
    def rt_rating(self,row):
        #print(row)
        row = str(row).decode('unicode_escape').encode('ascii','ignore')
        print("rt rating: {}".format(row))
        #from IPython.core.debugger import Tracer; Tracer()()
        rating = " "
        tomatometer = " "
        if row is not None:
            #Tomatometer
            match = re.search(r'\s*(\d+%).', row)
            if match is not None:
                tomatometer = match.group(1)
            #Average Rating
            match = re.search(r'(\d+\.\d+)/(\d+)', row)
            if match is not None:
                rating = match.group(1)
            else:
                match = re.search(r'(\d+)/(\d+)', row)
                if match is not None:
                    rating = match.group(1)
        return pd.Series({'RT':rating, 'Tomatometer':tomatometer})

    
    def clean_movie(self):
        # Cleaning up the scraped columns
        extra_info_name = self.inputMovieList.apply(lambda x: self.movie_name(x['Release Name']), axis=1)
        extra_info_rating = self.inputMovieList.apply(lambda x: self.imdb_rating(x['IMDB Rating']), axis=1)
        extra_info_rt = self.inputMovieList.apply(lambda x: self.rt_rating(x['RT Critics']), axis=1)
        movies_extra_info = pd.concat([self.inputMovieList,extra_info_name,extra_info_rating,extra_info_rt], axis =1)
        
        # ### Removing Duplicates
        
        movies_extra_info[['IMDB','Year','Votes']] = movies_extra_info[['IMDB','Year','Votes']].convert_objects(convert_numeric=True)
        #std_resolution = ['1080p','780p','BDRip','BRRip','DVDRip','HC','HDRip','BluRay','HDCAM','WEBDL','UNRATED','HDTS','480p','3D','WebRip',""]
        #rank_resolution = {'1080p':1,'780p':2,'BDRip':4,'BRRip':3,'BluRay':5,'DVDRip':6,'HC':8,'HDRip':7,'WebRip':12,'WEBDL':11,'UNRATED':9,'480p':10,'':13}
        #for index, row in movies_scraped_extra_info.iterrows():
        #if movies_scraped_extra_info['Resolution'] is not None:
        # movies_extra_info['Resolution'] = movies_extra_info.Resolution.map(
        #     lambda x: (difflib.get_close_matches(x,std_resolution)[0] if len(difflib.get_close_matches(x,std_resolution))>0 else ""))

        #vote_mask = movies_extra_info['Votes'] > self.minVotes
        #rating_mask = movies_extra_info['IMDB'] > self.minRating
        
        ##Removing entries with unwanted
        mask=None
        for res in self.avoid_list_of_releases:
            mask_curr = ~movies_extra_info['Release Type'].str.contains(res)
            if mask is None:
                mask = mask_curr
            else:
                mask = mask & mask_curr
        
        #mask = vote_mask & rating_mask & hdts_mask & hdcam_mask & three_d_mask
        #mask = vote_mask & rating_mask & hdts_mask & hdcam_mask & three_d_mask
        movies_extra_info = movies_extra_info[mask]
        ##Dropping duplicates after sorting with rank
        movies_extra_info['Res_Rank'] = movies_extra_info.Resolution.map(self.rank_list_of_releases)
        movies_extra_info['sort_name'] = movies_extra_info['Name'].str.lower()                 
        movies_extra_info.sort_values(['sort_name','Res_Rank'], ascending=[True,True], axis = 0, inplace=True)
        movies_extra_info.drop_duplicates('sort_name', keep ='first', inplace=True)
        movies_extra_info.reset_index(drop=True, inplace=True)

        
        cols = [ 'Name','Year', 'Genre', 'IMDB', 'Votes','RT Critics','Plot', 'Starring','Directed By', 
                'IMDB Link','RT Link', 'Post Link','Release Name','Release Type', 'Release Date','Thumbnail Link',
                'date_time','Trailer Link', 'Tomatometer','RT', 'post_date']
        self.cleanMovieList = movies_extra_info[cols]