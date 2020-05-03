import json,codecs
from datetime import datetime, timedelta
import time
from collections import deque
from pathlib import Path
import os
import requests

class CachingBatchProcessor:
    """ This class executes any function similarly to the inbuilt python map() function, executing element-wise across an input list. In addition, the target function is rate-limited, executed in custom batches with periodic breaks between batches. Lastly, the outputs of the function are cached and regularly saved to disk, rather than being held in memory until completion of the map.

    """    
    def __init__(self,target_batch_size = 200, seconds_per_batch = 300, target_cache_size = 1000):
        self.target_cache_size = target_cache_size
        self.target_batch_size = target_batch_size
        self.seconds_per_batch = seconds_per_batch

        self.current_requests = 0
        self.cache_number = 0
        self.current_cache_size = 0
        self.cache = deque()
    


    def map(self,func,data,save_path):
        """ Maps a function across a dataset, caches & saves outputs regularly, while rate limiting function calls

        Arguments:
            func {function(a)} -- The function to batch
            data {list(a)} -- An list of inputs to be processed by func one at a time
            save_path {string} -- The save location for cached outputs
        """
        batch_starttime = datetime.now()
        for element in data:

            # If we've hit the full batch, wait to start a new batch
            if(self.current_requests==self.target_batch_size):
                batch_endtime = datetime.now()
                timedelta = batch_endtime-batch_starttime;
                time_to_wait = self.seconds_per_batch - (timedelta.total_seconds())
                print('time to wait: '+str(time_to_wait))
                time.sleep(max(time_to_wait,0))

                # Reset tracking metrics for a new batch
                self.current_requests=0
                batch_starttime = datetime.now()

            try:
                self.current_requests = self.current_requests+1
                print('current reqs: '+str(self.current_requests))
                
                # Attempt the function proper 
                out = func(element)
            except:
                # func(element) throws an error, attempt func(element) on the next element
                print('Continuing to next element')
                continue
                
            if out is not None:
                self.cache.append(out)
                self.current_cache_size = self.current_cache_size+1
                print('Appending '+str(out))
                print('Number in cache '+str(self.current_cache_size))
            
            if(self.current_cache_size==self.target_cache_size):
                self._save_cache(save_path)

        # After all elements have been processed, ensure the final cache is saved
        if self.current_cache_size < target_cache_size:
            self._save_cache(save_path)

    def _save_cache(self,save_path):
        """Saves the contents of the executed func cache to disk

        Arguments:
            save_path {string} -- The path to a directory in which to save output
        """
        abs_path = (os.path.abspath(save_path))
        Path(abs_path).mkdir(parents=True,exist_ok=True)
        
        # New file save path
        save_path = '{}/cache_{}.txt'.format(abs_path,self.cache_number)

        with open(save_path, 'w') as f:
            for item in self.cache:
                f.write(str(item)+'\n')
        
        self.current_cache_size = 0
        self.cache_number = self.cache_number+1
        self.cache = deque()

    # def _attempt_func_internal(self,func, element, i, timeout, current_iter):
    #     try:
    #         return func(element)
    #     except TypeError:
    #         if current_iter==i:
    #             print('Excessive nulls, raising')
    #             raise
    #         else:
    #             print('Null value, waiting')
    #             time.sleep(timeout/1000)
    #     _attempt_func_internal(func,element,i,timeout,current_iter+1)

    # def _attempt_func(self,func,element,i=0,timeout=300):
    #     _attempt_func_internal(func,element,i,timeout,0)


        
class SteamGameScraper:
    """This class access the steampowered API to request details about a particular steam game
    """
    def __init__(self, scrape_properties):
        self.scrape_properties = scrape_properties

    def scrape(self,data):
        """Acquires a game's details from the store.steampowered API. Discards non-game titles.

        Arguments:
            data {dict} -- Dict of appid & game title, previously acquired from a different API

        Returns:
            dict -- Key-value pair of a game's properties
        """
        appid = str(data['appid'])

        # Make store.steampowered api call
        response = requests.post('https://store.steampowered.com/api/appdetails/?appids='+appid)
        game_data = response.json()[appid]

        if game_data['success'] == True:
            is_game = game_data['data']['type']=='game'
            if is_game:
                return self._append_properties(data,game_data)

        return None

    def _append_properties(self,data,game_data):
        """Appends additional game-details to the existing appid/title dict

        Arguments:
            data {dict} -- Dict of appid & game title, previously acquired from a different API
            game_data {json} -- Steam API response for the appid of the input data

        Returns:
            dict -- Dict of an app's appid, game title, and all chosen properties to extract
        """
        for prop in self.scrape_properties:
            try:
                data[prop] = game_data['data'][prop]
            except:
                data[prop] = None
            
        return data



if __name__ == '__main__':

    f = codecs.open('../data/applist.json','r','utf-8')
    data = json.load(f, encoding='utf-8')
    f.close()

    datetime = datetime.now()
    formatted_datetime = datetime.strftime("%Y-%m-%d_%H-%M-%S")

    cache_path = '../data/cache/{}/'.format(formatted_datetime)

    scrape_features = ['is_free','developers','supported_languages','platforms','genres','categories','recommendations','price_overview','release_date']
    
    scraper = SteamGameScraper(scrape_features)
    caching_processor = CachingBatchProcessor()
    caching_processor.map(scraper.scrape,data['applist']['apps'],cache_path)
