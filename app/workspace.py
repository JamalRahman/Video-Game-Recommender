from ml.models import Dummy, LogReg, NN
import numpy as np
import json
import codecs
import steamspypi

# model = LogReg()
# xs = list(range(10,30))
# ys = (([0]*10)+([1]*10))

# model.train(np.reshape(xs,(-1,1)),ys)

# out = model.predict([[11],[23],[29]])

# print(out)

data_request = dict()
data_request['request'] = 'all'

data = steamspypi.download(data_request)
len(data))