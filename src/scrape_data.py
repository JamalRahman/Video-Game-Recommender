import json,codecs
from datetime import datetime, timedelta
import time
from collections import deque
from pathlib import Path
import os

def cache_batch(batch, path):

    # Make directories for saving batches
    abs_path = (os.path.abspath(path))
    Path(abs_path).mkdir(parents=True,exist_ok=True)
    save_path = '{}/batch_{}.txt'.format(abs_path,batch_number)

    print("Saving batch "+str(batch_number)+'to location '+str(save_path))
    with open(save_path, 'w') as f:
        for item in batch:
            f.write(str(item))


f = codecs.open('data/applist.json','r','utf-8')
data = json.load(f, encoding='utf-8')
f.close()

print(len(data['applist']['apps']))

batch_size = 200
ms_per_batch = 1000

batch_starttime = datetime.now()
current_batch_count = 0
batch_number = 0
batch = deque()

formatted_datetime = batch_starttime.strftime("%Y-%m-%d_%H-%M-%S")
cache_path = 'data/cache/{}/'.format(formatted_datetime)
    

for app in data['applist']['apps']:
    if(current_batch_count==batch_size-1):
        # cache batch
        cache_batch(batch, cache_path)
        current_batch_count = 0
        batch_number = batch_number+1

        # wait for time_delta to hit ms_per_batch
        batch_endtime = datetime.now()
        timedelta = batch_endtime-batch_starttime;
        time_to_wait = ms_per_batch - (timedelta.microseconds / 1000)
        print('time to wait: '+str(time_to_wait))

        time.sleep(max(time_to_wait,0)/1000)

    if(batch_number>1):
        break;

    appid = app['appid']
    batch.append(appid)
    current_batch_count = current_batch_count+1

