from ml.models import Dummy, LogReg, NN
import numpy as np
import json
import codecs


# model = LogReg()
# xs = list(range(10,30))
# ys = (([0]*10)+([1]*10))

# model.train(np.reshape(xs,(-1,1)),ys)

# out = model.predict([[11],[23],[29]])

# print(out)

with codecs .open('data/applist.json','r','utf-8') as f:
    data = json.load(f, encoding='utf-8')
    print(len(data['applist']['apps']))
print('done')