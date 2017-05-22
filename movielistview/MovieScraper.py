# -*- coding: utf-8 -*-
"""
Created on Fri May 19 07:24:06 2017

@author: manuj
"""

import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sys
import re
from django.utils import timezone
from dateutil.parser import parse
import datefinder
import difflib
from datetime import datetime, timedelta
import time


class MovieScraper:
    
    movieScraped = pd.DataFrame()
    std_list_of_releases = ['CAMRip','CAM ','TS','TELESYNC','PDVD ','WP','WORKPRINT ','TC','TELECINE ',
                            'PPV','PPVRip ','SCR','SCREENER','DVDSCR','DVDSCREENER','BDSCR ','DDC ','R5',
                            'R5.LINE','R5.AC3.5.1.HQ ','DVDRip ','DVDR','DVD-Full','Full-Rip','ISO rip',
                            'untouched rip','DSR','DSRip','SATRip','DTHRip','DVBRip','HDTV','PDTV','TVRip',
                            'HDTVRip ','VODRip','VODR ','WEBDL','WEB DL','WEB-DL','HDRip ','WEBRip (P2P)',
                            'WEB Rip (P2P)','WEB-Rip (P2P)','WEB (Scene) ','WEB-Cap','WEBCAP','WEB Cap ',
                            'BDRip','BRRip','Blu-Ray','BluRay','BLURAY','BDMV','BDR']

    @classmethod
    def __init__(self):
        stdout = sys.stdout
        reload(sys)
        sys.setdefaultencoding('utf-8')
        sys.stdout = stdout

    @classmethod
    def find_release_type_from_name(self,name,std_list_of_release_names):
        std_list_of_release_names = [x.upper() for x in std_list_of_release_names]
        release = ""
        release_score = 0
        for part in name.upper().split('.'):
            if len(difflib.get_close_matches(part,std_list_of_release_names,1,0.8))==1:
                curr_release = difflib.get_close_matches(part,std_list_of_release_names,1,0.8)[0]
                curr_release_score = difflib.SequenceMatcher(None,curr_release, part).ratio()
                if curr_release_score > release_score:
                    release_score = curr_release_score
                    release = curr_release
        return release


    @classmethod
    def scrape_page(self,url,scrape_list, post_date):
        entry_dict = {}
        try :
            print('SETTING UP PROXY')
            #proxy = urllib2.ProxyHandler({'https': 'https://www.proxysite.com/'})
            #opener = urllib2.build_opener(proxy)
            #urllib2.install_opener(opener)
            candidate_proxies = ['https://www.proxysite.com/',
                     'https://www.freeproxyserver.co/']
            for proxy in candidate_proxies:
                print "Trying HTTP proxy %s" % proxy
                try:
                    web_page = urllib.urlopen(url, proxies={'http': proxy})
                    print "Got URL using proxy %s" % proxy
                    break
                except:
                    print "Trying next proxy in 5 seconds"
                    time.sleep(5)


            #print('SENDING REQ') #ADd timeout
            #req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"}) 
            #web_page = urllib2.urlopen(req)
            #print('OPENING WEBPAGE')
            soup = BeautifulSoup(web_page,'html.parser')
            divs = soup.find('div', id='recent-posts')
            entries = divs.findAll('div', { "class" : "entry" })
            for entry in entries:
                entry_dict = {}
                entry_content = entry.find('div' , {"class" : "entry-content"})
                post_link = entry.find('h2' , {"class" : "title"}).find('a').get('href')
                entry_dict['Post Link'] = post_link
                meta_divs = entry_content.findAll('div', {"class" : "meta"})
                post_meta = entry.findNext('div', {'class':"post-meta"})
                release_info = ""
                release_desc = ""
                link_div = None
                for div in meta_divs:
                    match = re.search(r'\s*[Rr]elease\s+[Ii]nfo\s*', str(div.get_text))
                    if match is not None:
                        thumbnail = div.findNext("p").find_next('a').get('href')
                        entry_dict['Thumbnail Link'] = thumbnail
                        release_info = div.findNext("p").get_text()
                    match = re.search(r'\s*[Rr]elease\s+[Dd]escription\s*', str(div.get_text))
                    if match is not None:
                        release_desc = div.findNext("p").get_text()
                    match = re.search(r'\s*[Aa]ssociated\s+[Ll]inks\s*', str(div.get_text))
                    if match is not None:
                        link_div = div.findNext("p")
           
                release_info = release_info.decode('unicode_escape').encode('ascii','ignore')
                release_desc = release_desc.decode('unicode_escape').encode('ascii','ignore')
                entry_dict['Plot'] = release_desc
                items = re.split(r'\s*\n\s*', release_info)
                for item in items:
                    dict_items = re.split(r'\s*:\s*',item)
                    if len(dict_items) > 1:
                        entry_dict[dict_items[0]] = dict_items[1]
                if 'Release Name' in entry_dict:
                    entry_dict['Release Type'] = self.find_release_type_from_name(entry_dict['Release Name'], self.std_list_of_releases)
                if 'Release Date' in entry_dict:
                    try:
                        if entry_dict['Release Date'] is not None:
                            entry_dict['Release Date'] = parse(entry_dict['Release Date'])
                    except ValueError:
                        entry_dict['Release Date'] = np.nan
                #parsing links
                if link_div is not None:
                    links =link_div.findAll('a')
                    for link in links:
                        link_text = link.get_text()
                        match = re.search(r'[Ii][Mm][Dd][Bb]',link_text)
                        if match is not None:
                            entry_dict['IMDB Link'] = link.get('href')
                        match = re.search(r'[Rr][Tt]',link_text)
                        if match is not None:
                            entry_dict['RT Link'] = link.get('href')
                        match = re.search(r'[Tt][Rr][Aa][Ii][Ll][Ee][Rr]',link_text)
                        if match is not None:
                            entry_dict['Trailer Link'] = link.get('href')
                #Parsing Post Date
                matches = datefinder.find_dates(post_meta.text)
                for match in matches:
                    entry_dict['post_date'] = match
                    break
                entry_dict['date_time'] = datetime.now()
                # #Debug
                # entry_dict['post_meta'] = post_meta.text
                #if condition to stop scraping once date is hit
                if entry_dict['post_date'] > last_date - timedelta(days=1):
                    scrape_list.append(entry_dict)
                else:
                    break
            return scrape_list
        except urllib2.HTTPError as err :
            print("HTTPERROR!")
            print(err.code)
            return 0
        except urllib2.URLError :
            print("URLERROR!")
            return 0
    
    @classmethod
    def scrape_site(self,pages,post_date):
        scraped_movies = []
        scraped_movies = self.scrape_page('http://sceper.ws/category/movies',scraped_movies,post_date) #Replace with date
        print("scrape first page done")
        #from progressbar import ProgressBar
        #pbar = ProgressBar()
        #for x in pbar(range(2,pages)):
        for x in range(2,pages):
            print(x)
            page_url = 'http://sceper.ws/category/movies/page/' + str(x)
            scraped_movies = self.scrape_page(page_url,scraped_movies,post_date) #Replace with date
            
        self.movieScraped = pd.DataFrame.from_dict(scraped_movies)
        
#Calling the main function
#movie_scraped = MovieScraper()
#movie_scraped.scrape_site(5)
#print(movie_scraped.movieScraped.count())