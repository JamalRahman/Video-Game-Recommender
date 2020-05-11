# import data
# Augment data with preprocessing
# Data test/train split
# Build CNN
import tensorflow as tf
from sklearn.linear_model import LogisticRegression

class Model():
    def __init__ (self,path:str=None):
        self._model = None
        self._path = path

        if(self._path != None):
            self.load()
    
    def train(self,xs,ys):

        pass
    
    def predict(self, x):
        pass

    def save(self,path):

        pass

    def load(self):
        pass

class NN(Model):

    def predict(self, x):
        pass

    def load(self):
        try:
            self._model = tf.saved_model.load(self._path)
        except:
            raise
        return self
    pass

class Dummy(Model):

    def predict(self, x):
        return 2*x
    pass

class LogReg(Model):

    def train(self, xs, ys):
        self._model = LogisticRegression()
        self._model.fit(xs,ys)
        
    def predict(self, x):
        return self._model.predict(x)