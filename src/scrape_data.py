import json,codecs
from datetime import datetime, timedelta
import time
from collections import deque
from pathlib import Path
import os
import requests

class BatchProcessor:
    def __init__(self,target_batch_size = 200, ms_per_batch = 300000):
        self.target_batch_size = target_batch_size
        self.ms_per_batch = ms_per_batch

        self.current_batch_size = 0
        self.batches_made = 0
        self.batch = deque()
    
    def process_batches(self,func,data,save_path):
        batch_starttime = datetime.now()
        for element in data:
            # Get response
            # Parse game from response
            out = func(element)

            if out is not None:
                self.batch.append(out)
                self.current_batch_size = self.current_batch_size+1
                print('Appending '+str(out))
                print('Current in batch '+str(self.current_batch_size))
            
            if(self.current_batch_size==self.target_batch_size):
                # save batch
                self.save_batch(save_path)
                current_batch_size = 0
                # wait for time_delta to hit ms_per_batch
                batch_endtime = datetime.now()
                timedelta = batch_endtime-batch_starttime;
                time_to_wait = ms_per_batch - (timedelta.microseconds / 1000)
                print('time to wait: '+str(time_to_wait))
                time.sleep(max(time_to_wait,0)/1000)

        if self.current_batch_size < target_batch_size:
            self.save_batch(save_path)
        
    def save_batch(self,save_path):
        abs_path = (os.path.abspath(path))
        Path(abs_path).mkdir(parents=True,exist_ok=True)
        
        # New file save path
        save_path = '{}/batch_{}.txt'.format(abs_path,batch_number)

        with open(save_path, 'w') as f:
            for item in batch:
                f.write(str(item))
        
        self.current_batch_size = 0
        self.batch_number = batch_number+1
        
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
                return self.extract_features(data,game_data)
        return None

            
    def extract_features(self,data,game_data):
        data['is_game'] = (game_data['data']['type']=='game')

        return data



if __name__ == '__main__':

    f = codecs.open('data/applist.json','r','utf-8')
    data = json.load(f, encoding='utf-8')
    f.close()

    datetime = datetime.now()
    formatted_datetime = datetime.strftime("%Y-%m-%d_%H-%M-%S")

    cache_path = 'data/cache/{}/'.format(formatted_datetime)
    scraper = SteamScraper()
    batch_processor = BatchProcessor()

    batch_processor.process_batches(scraper.scrape,data['applist']['apps'],cache_path)
