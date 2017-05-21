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


class MovieScraper:
    
    movieScraped = pd.DataFrame()
    @classmethod
    def __init__(self):
        stdout = sys.stdout
        reload(sys)
        sys.setdefaultencoding('utf-8')
        sys.stdout = stdout
    
    @classmethod
    def scrape_page(self,url,scrape_list):
        entry_dict = {}
        try :
            
            proxy = urllib2.ProxyHandler({'https': 'https://www.proxysite.com/'})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)

            req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"}) 
            web_page = urllib2.urlopen(req)
            soup = BeautifulSoup(web_page,'html.parser')
            divs = soup.find('div', id='recent-posts')
            entries = divs.findAll('div', { "class" : "entry" })
            for entry in entries:
                entry_dict = {}
                entry_content = entry.find('div' , {"class" : "entry-content"})
                post_link = entry.find('h2' , {"class" : "title"}).find('a').get('href')
                entry_dict['Post Link'] = post_link
                meta_divs = entry_content.findAll('div', {"class" : "meta"})
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
                
                #entry_dict['date_time'] = datetime.datetime.now()
                entry_dict['date_time'] = timezone.now()
                scrape_list.append(entry_dict)
            return scrape_list
        except urllib2.HTTPError :
            print("HTTPERROR!")
            return 0
        except urllib2.URLError :
            print("URLERROR!")
            return 0
    
    @classmethod
    def scrape_site(self,pages):
        scraped_movies = []
        scraped_movies = self.scrape_page('http://sceper.ws/category/movies',scraped_movies)
        #from progressbar import ProgressBar
        #pbar = ProgressBar()
        #for x in pbar(range(2,pages)):
        for x in range(2,pages):
            print(x)
            page_url = 'http://sceper.ws/category/movies/page/' + str(x)
            scraped_movies = self.scrape_page(page_url,scraped_movies)
            
        self.movieScraped = pd.DataFrame.from_dict(scraped_movies)
        
#Calling the main function
#movie_scraped = MovieScraper()
#movie_scraped.scrape_site(5)
#print(movie_scraped.movieScraped.count())