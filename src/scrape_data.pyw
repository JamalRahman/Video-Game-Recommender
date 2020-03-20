import json,codecs
from datetime import datetime, timedelta
import time
from collections import deque
from pathlib import Path
import os
import requests

def attempt_func(func,element,iter=0):
    try:
        return func(element)
    except TypeError:
        if iter==3:
            raise RuntimeError
        else: pass
    attempt_func(func,element,iter+1)


class BatchProcessor:
    def __init__(self,target_batch_size = 200, ms_per_batch = 300000):
        self.target_batch_size = target_batch_size
        self.ms_per_batch = ms_per_batch

        self.batch_number = 0
        self.current_batch_size = 0
        self.batches_made = 0
        self.batch = deque()
    

    def process_batches(self,func,data,save_path):
        self.batch_starttime = datetime.now()
        for element in data:

            if self.batch_number>0:
                return

            # Get response
            # Parse game from response
            try:
                out = attempt_func(func,element)

            except TypeError:
                # Too many requests, wait then try again.
                time.sleep(ms_per_batch/1000)
                
            if out is not None:
                self.batch.append(out)
                self.current_batch_size = self.current_batch_size+1
                print('Appending '+str(out))
                print('Current in batch '+str(self.current_batch_size))
            
            if(self.current_batch_size==self.target_batch_size):
                # save batch
                
                self.save_batch(save_path)

                # wait for time_delta to hit ms_per_batch
                time_to_wait = self.ms_per_batch - (self.timedelta.total_seconds() * 1000)
                print('time to wait: '+str(time_to_wait))
                time.sleep(max(time_to_wait,0)/1000)

        if self.current_batch_size < target_batch_size:
            self.save_batch(save_path)

    def save_batch(self,save_path):
        abs_path = (os.path.abspath(save_path))
        Path(abs_path).mkdir(parents=True,exist_ok=True)
        
        # New file save path
        save_path = '{}/batch_{}.txt'.format(abs_path,self.batch_number)

        with open(save_path, 'w') as f:
            for item in self.batch:
                f.write(str(item)+'\n')
        
        self.current_batch_size = 0
        self.batch_number = self.batch_number+1

        batch_endtime = datetime.now()
        self.timedelta = batch_endtime-self.batch_starttime;
        self.batch_starttime = datetime.now()
        
class SteamScraper:

    def scrape(self,data):
        appid = str(data['appid'])

        # Make store.steampowered api call
        response = requests.post('https://store.steampowered.com/api/appdetails/?appids='+appid)

        # POTENTIAL TYPERROR HERE
        game_data = response.json()[appid]
        if game_data['success'] == True:
            # Get game info
            # Add game info to batch
            is_game = game_data['data']['type']=='game'
            if is_game:
                return self._extract_features(data,game_data)
        return None

    def _extract_features(self,data,game_data):
        data['is_free'] = self._get_key(game_data['data'],'is_free')
        data['developers'] = self._get_key(game_data['data'],'developers')
        data['languages'] = self._get_key(game_data['data'],'supported_languages')
        data['platforms'] = self._get_key(game_data['data'],'platforms')
        data['genres'] = self._get_key(game_data['data'],'genres')
        data['categories'] =self._get_key(game_data['data'],'categories')
        return data

    def _get_key(self,json,key):
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
    batch_processor = BatchProcessor(200)

    batch_processor.process_batches(scraper.scrape,data['applist']['apps'],cache_path)
