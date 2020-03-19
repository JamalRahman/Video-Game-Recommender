import json,codecs
from datetime import datetime, timedelta
import time
from collections import deque
from pathlib import Path
import os
import requests


class GameScraper:
    def __init__(batch_size, ms_per_batch):
        self.batch_size = batch_size
        self.ms_per_batch = ms_per_batch
        self.current_batch_size = 0
        self.batches_made = 0
        self.batch = deque()

    def scrape(data):
        for app in data:

            if(batches_made>0):
                break;

            appid = str(app['appid'])
            
            # Make store.steampowered api call
            response = requests.post('https://store.steampowered.com/api/appdetails/?appids='+appid)

            game_info = response.json()[appid]
            if game_info['success'] == True:
                is_game = game_info['data']['type']=='game'
                print(app['name']+' '+str(is_game))

                if is_game:
                    app['is_game'] = int(is_game)
                    batch.append(app)
                    current_batch_size = current_batch_size+1

            is_game = scraper.is_game(response)

            if(self.current_batch_size==self.batch_size-1):
                # cache batch
                scraper.save_batch(batch, cache_path)

                # wait for time_delta to hit ms_per_batch
                batch_endtime = datetime.now()

                timedelta = batch_endtime-batch_starttime;
                time_to_wait = ms_per_batch - (timedelta.microseconds / 1000)
                print('time to wait: '+str(time_to_wait))

                time.sleep(max(time_to_wait,0)/1000)

    def save_batch(batch, path):

        # Make directories for saving batches
        abs_path = (os.path.abspath(path))
        Path(abs_path).mkdir(parents=True,exist_ok=True)
        
        # New file save path
        save_path = '{}/batch_{}.txt'.format(abs_path,batch_number)

        with open(save_path, 'w') as f:
            for item in batch:
                f.write(str(item))
        
        self.current_batch_size = 0
        self.batch_number = batch_number+1

    def is_game(appid,batch):
        pass





if __name__ == '__main__':

    f = codecs.open('data/applist.json','r','utf-8')
    data = json.load(f, encoding='utf-8')
    f.close()

    batch_starttime = datetime.now()
    formatted_datetime = batch_starttime.strftime("%Y-%m-%d_%H-%M-%S")

    cache_path = 'data/cache/{}/'.format(formatted_datetime)
    
    scraper = GameScraper()
    scraper.scrape(data['applist']['apps'])
        

            # Assume we tried going too fast, so pause for 5 minutes and retry last.
        