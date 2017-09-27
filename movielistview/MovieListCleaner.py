# coding: utf-8

# ### Cleaning the scraped list

import pandas as pd
import re




class MovieListCleaner:
    
    inputMovieList = pd.DataFrame()
    cleanMovieList = pd.DataFrame()

    rank_list_of_releases = {'HD-TC':62,'HDTC':61,'CAMRip':60 ,'CAM':59,'HDCAM':58,'TS':57,'HDTS':56, 'HD-TS':55,'TELESYNC':54,'PDVD':53,'WP':52,'WORKPRINT':51,'TC':50,'TELECINE':49,
                            'PPV':48,'PPVRip':47,'SCR':46,'SCREENER':45,'DVDSCR':44,'DVDSCREENER':43,'BDSCR':42,'DDC':41,'R5':40,
                            'R5.LINE':39,'R5.AC3.5.1.HQ':38,'DVDRip':37,'DVDR':36,'DVD-Full':35,'Full-Rip':34,'ISO rip':33,
                            'untouched rip':32,'DSR':31,'DSRip':30,'SATRip':29,'DTHRip':28,'DVBRip':27,'HDTV':26,'PDTV':25,'TVRip':24,
                            'HDTVRip':23,'VODRip':22,'VODR':21,'WEB':20,'WEBDL':19,'WEB DL':18,'WEB-DL':17,'HDRip':16,'WEBRip':15,'WEBRip (P2P)':14,
                            'WEB Rip (P2P)':13,'WEB-Rip (P2P)':12,'WEB (Scene)':11,'WEB-Cap':10,'WEBCAP':9,'WEB Cap':8,
                            'BDRip':7,'BRRip':6,'Blu-Ray':5,'BluRay':4,'BLURAY':3,'BDMV':2,'BDR':1}

    avoid_list_of_releases = ['CAMRip','CAM','HDCAM','TS', 'HDTS','HD-TS','HDTC','HD-TC','TELESYNC','PDVD','WP','WORKPRINT','TC','TELECINE',
                            'PPV','PPVRip ','SCR','SCREENER','DVDSCR','DVDSCREENER','BDSCR ','DDC','R5',
                            'R5.LINE','R5.AC3.5.1.HQ']


    
    def __init__(self,df):
        self.inputMovieList = df
        self.rank_list_of_releases.update([(k.upper(), v) for k, v in self.rank_list_of_releases.iteritems()])
        self.avoid_list_of_releases = [x.upper() for x in self.avoid_list_of_releases]


    # ### Extracting Movie Name and other details from the file name   
    def movie_name(self,row):
    	print row
        n=""
        resolution = ""
        year = 0
        match_found = False
        res_bool = False
        if row is not None:
            for part in str(row).split("."):
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
        return pd.Series({'Name':str(n),'Year':str(year),'Resolution':str(resolution)})

# ### Extracting IMDB Rating
    
    def imdb_rating(self,row):
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
        row = str(row).decode('unicode_escape').encode('ascii','ignore')
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
                else:
                    rating = 0
        return pd.Series({'RT':rating, 'Tomatometer':tomatometer})

    
    def clean_movie(self):
        # Cleaning up the scraped columns
        extra_info_name = self.inputMovieList.apply(lambda x: self.movie_name(x['Release Name']), axis=1)
        extra_info_rating = self.inputMovieList.apply(lambda x: self.imdb_rating(x['IMDB Rating']), axis=1)
        extra_info_rt = self.inputMovieList.apply(lambda x: self.rt_rating(x['RT Critics']), axis=1)
        movies_extra_info = pd.concat([self.inputMovieList,extra_info_name,extra_info_rating,extra_info_rt], axis =1)
        
        # ### Removing Duplicates
        
        movies_extra_info[['IMDB','Year','Votes','RT']] = movies_extra_info[['IMDB','Year','Votes','RT']].convert_objects(convert_numeric=True)
        
        ##Removing entries with unwanted
        mask=None
        for res in self.avoid_list_of_releases:
            mask_curr = ~movies_extra_info['Release Type'].str.contains(res)
            if mask is None:
                mask = mask_curr
            else:
                mask = mask & mask_curr
        
        movies_extra_info = movies_extra_info[mask]
        ##Dropping duplicates after sorting with rank
        movies_extra_info = self.remove_duplicates(movies_extra_info)


        
        cols = [ 'Name','Year', 'Genre', 'IMDB', 'Votes','RT Critics','Plot', 'Starring','Directed By', 
                'IMDB Link','RT Link', 'Post Link','Release Name','Release Type', 'Release Date','Thumbnail Link',
                'date_time','Trailer Link', 'Tomatometer','RT', 'post_date']
        self.cleanMovieList = movies_extra_info[cols]


    def remove_duplicates(self, df):
        ##Dropping duplicates after sorting with rank
        df['Res_Rank'] = df['Release Type'].map(lambda x: x.strip()).map(str.strip).map(self.rank_list_of_releases)
        df['sort_name'] = df['Name'].str.lower()                 
        df.sort_values(['sort_name','Res_Rank'], ascending=[True,True], axis = 0, inplace=True)
        df.drop_duplicates('sort_name', keep ='first', inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def remove_duplicates_model(self, df):
        ##Dropping duplicates after sorting with rank from model
        df['Res_Rank'] = df.release_type.map(lambda x: x.strip()).map(self.rank_list_of_releases)
        df['sort_name'] = df['name'].str.lower()                 
        df.sort_values(['sort_name','Res_Rank'], ascending=[True,True], axis = 0, inplace=True)
        df.drop_duplicates('sort_name', keep ='first', inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
