import json,codecs
from datetime import datetime, timedelta
import time
from collections import deque
from pathlib import Path
import os
import requests


def attempt_func(func,element,iter=0,timeout=300):
    try:
        return func(element)
    except TypeError:
        if iter==0:
            print('Excessive nulls, raising')
            raise
        else:
            print('Null value, waiting')
            time.sleep(timeout/1000)
    attempt_func(func,element,iter+1)


class CachingBatchProcessor:
    def __init__(self,target_batch_size = 200, ms_per_req_batch = 300):
        self.target_cache_size = 1000

        self.target_batch_size = target_batch_size
        self.ms_per_req_batch = ms_per_req_batch
        self.current_requests = 0

        self.cache_number = 0
        self.current_cache_size = 0
        self.caches_made = 0
        self.cache = deque()
    


    def cache_process(self,func,data,save_path):
        batch_starttime = datetime.now()
        for element in data:

            # If we've hit the full batch, wait to start a new batch
            if(self.current_requests==self.target_batch_size):
                # wait for time_delta to hit ms_per_batch

                batch_endtime = datetime.now()
                timedelta = batch_endtime-batch_starttime;
                time_to_wait = self.ms_per_req_batch - (timedelta.total_seconds())
                print('time to wait: '+str(time_to_wait))
                time.sleep(max(time_to_wait,0))
                self.current_requests=0
                batch_starttime = datetime.now()

            try:
                self.current_requests = self.current_requests+1
                print('current reqs: '+str(self.current_requests))
                out = func(element)
                # self.error_flag = False
            except:
                # func(element) returned null more than n times, assume that element truly returns null, skip it
                # if self.error_flag:
                    # raise
                # else:
                print('Continuing to next element')
                    # self.error_flag = True
                continue
                
            if out is not None:
                self.cache.append(out)
                self.current_cache_size = self.current_cache_size+1
                print('Appending '+str(out))
                print('Number in cache '+str(self.current_cache_size))
            
            if(self.current_cache_size==self.target_cache_size):
                # save cache
                
                self.save_cache(save_path)



        if self.current_cache_size < target_cache_size:
            self.save_cache(save_path)

    def save_cache(self,save_path):
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


        
class SteamScraper:

    def __init__(self):
        self.features = ['is_free','developers','supported_languages','platforms','genres','categories','recommendations','price_overview','release_date']

    def scrape(self,data):
        appid = str(data['appid'])

        # Make store.steampowered api call
        response = requests.post('https://store.steampowered.com/api/appdetails/?appids='+appid)
        game_data = response.json()[appid]

        if game_data['success'] == True:
            is_game = game_data['data']['type']=='game'
            if is_game:
                return self._extract_features(self.features,data,game_data)

        return None

    def _extract_features(self,features,data,game_data):
        extracted = {}
        for feature in features:
            data[feature] = self._get_value(game_data['data'],feature)
        return data

    def _get_value(self,json,key):
        try:
            return json[key]
        except:
            return None
            



if __name__ == '__main__':

    f = codecs.open('../data/applist.json','r','utf-8')
    data = json.load(f, encoding='utf-8')
    f.close()

    datetime = datetime.now()
    formatted_datetime = datetime.strftime("%Y-%m-%d_%H-%M-%S")

    cache_path = '../data/cache/{}/'.format(formatted_datetime)
    scraper = SteamScraper()
    caching_processor = CachingBatchProcessor()
    caching_processor.cache_process(scraper.scrape,data['applist']['apps'],cache_path)
