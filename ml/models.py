# import data
# Augment data with preprocessing
# Data test/train split
# Build CNN

from abc import ABC, abstractmethod

class Model(ABC):

    @abstractmethod
    def train(self,xs,ys):
        pass
    
    @abstractmethod
    def predict(self, x):
        pass

    def save(self):
        # model.save
        pass

    @abstractmethod
    def load(self):
        # model 
        pass

class CNN(Model):
    def train(self, xs, ys):
        return super().train(xs, ys)
    def predict(self, x):
        return super().predict(x)
    def load(self):
        return super().load()
    pass