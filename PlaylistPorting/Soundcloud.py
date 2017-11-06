from Song import Song
import re
import difflib
import time
import urllib2
from bs4 import BeautifulSoup
import sys
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import quote_plus as qp
    raw_input = input
else:
    from urllib2 import urlopen
    from urllib import quote_plus as qp

import logging
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Soundcloud:

    def search_soundcloud(self,query, max_results):
        url = "https://soundcloud.com/search/sounds?q={}".format(query.replace(" ", "%20"))
        web_page = self.request_website(url,3)
        if web_page:
          soup = BeautifulSoup(web_page,'html.parser')
          search_list = soup.findAll('li')
          result_counter = 0
          results = []
          for li in search_list:
        #         print(li.get_text())
              everything = 'Everything' in li.get_text()
              tracks = 'Tracks' in li.get_text()
              playlists = 'Playlists' in li.get_text()
              people = 'People' in li.get_text()
              flag = not(everything|tracks|playlists|people)
              if flag:
                  result_counter = result_counter+1
                  a_tag = li.find_next('a')
                  song = Song("www.soundcloud.com{}".format(a_tag['href']), a_tag.get_text())
                  results.append(song)
                  if result_counter >= max_results:
                      break
          return results
        else:
          logger.info('No results Found in Soundcloud')    
          return None


    def get_soundcloud_song(self,title):
      #Searching in Soundcloud
      try:
          search_results = self.search_soundcloud(title,1)
          if len(search_results)>0:
              song = search_results[0]
              score = difflib.SequenceMatcher(None,song.title.lower(),title.lower()).ratio()
              if score <0.5:
                  logger.warning(u"Soundcloud Title: {}, Actual Title: {}, Score: {}. No satisfactory results in Soundcloud".format(song.title,title,score))
                  return None
          else:
              logger.warning(u"No Results found in Soundcloud also for {}. Skipping..".format(title))
              return None
      except Exception:
          logger.warning(u"No Results found in Soundcloud also for {}. Skipping..".format(title))
          return None
      return song



    def get_title_soundcloud(self,url):
        web_page = self.request_website(url,3)
        if web_page:
          soup = BeautifulSoup(web_page,'html.parser')
          return soup.find('meta',{'property':'og:title'})['content']
        else:
          logger.info('No results Found in Soundcloud')    
          return None    

    def extract_soundcloud_link_from_text(self,item):
      match = re.search(r'((https|http)://soundcloud.\S+)', item)
      if match:
          return match.group(1)
      else:
          return None

    def request_website(self,url, max_attempts):
        attempts = 0
        while attempts < max_attempts+1:
            try :
                req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"}) 
                # print('Opening Page') #ADd timeout
                web_page = urllib2.urlopen(req, timeout=30)
                return web_page
                # print('Opened Page') #ADd timeout
                break
            except urllib2.HTTPError:
                    print("HTTP ERROR!")
                    # print(err.code)
                    attempts += 1
                    print("Retrying...")
                    time.sleep(5)
                    if attempts == max_attempts:
                        return None
            except urllib2.URLError :
                print("URL ERROR!")
                attempts += 1
                print("Retrying...")
                time.sleep(5)
                if attempts == max_attempts:
                    return None
            except Exception, e:
                print("An ERROR! {}".format(str(e)))
                attempts += 1
                print("Retrying...")
                time.sleep(5)
                if attempts == max_attempts:
                    return None