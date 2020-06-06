# import data
# Augment data with preprocessing
# Data test/train split
# Build CNN
import gensim.models as g
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import math
scaler = MinMaxScaler()

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


class TfidfEmbeddingsRecommender(Model):
    def __init__(self, path=None,app_data=None):
        super().__init__(path=path)
        if self._model is None:
            print('error handle me')
        self._app_data = app_data

    def predict(self, x):

        # Cast x as list

        positives = []
        negatives = []
    
        for pos in x:
            positives.append(self._model.docvecs[str(pos)])
        
        similarity = self._model.docvecs.most_similar(positive=positives, negative=negatives,topn=34071)
        
        similar_games = pd.DataFrame(similarity,columns=['appid','d2v_similarity'])
        similar_games['appid'] = similar_games['appid'].astype(int)

        similar_games = similar_games.merge(self._app_data[['appid','name','positive']], how='left',on='appid')
        
        
        # ADD SCALED POSITIVES TO BASE APP_DATA. A lot of unnecessary scaling at runtime every model-call

        similar_games['scaled_positives'] = similar_games['positive']+1
        similar_games['scaled_positives'] = similar_games['scaled_positives'].apply(math.log)
        similar_games['scaled_positives'] = scaler.fit_transform(similar_games['scaled_positives'].values.reshape(-1,1))

        similar_games['score'] = similar_games['d2v_similarity']+ 0.26*similar_games['scaled_positives']
        
        similar_games = similar_games.sort_values(by='score',ascending=False)
        return list(similar_games['name'])[:10]

    def load(self):
        self._model = g.Doc2Vec.load(self._path)


class EmbeddingsRecommender(Model):

    def __init__(self, path=None,app_data=None):
        super().__init__(path=path)
        if self._model is None:
            print('error handle me')
        self._app_data = app_data

    def predict(self, x):

        # Cast x as list

        positives = []
        negatives = []
    
        for pos in x:
            positives.append(self._model.docvecs[str(pos)])
        
        similarity = self._model.docvecs.most_similar(positive=positives, negative=negatives,topn=34071)
        
        similar_games = pd.DataFrame(similarity,columns=['appid','d2v_similarity'])
        similar_games['appid'] = similar_games['appid'].astype(int)

        similar_games = similar_games.merge(self._app_data[['appid','name','positive']], how='left',on='appid')
        
        
        # ADD SCALED POSITIVES TO BASE APP_DATA. A lot of unnecessary scaling at runtime every model-call

        similar_games['scaled_positives'] = similar_games['positive']+1
        similar_games['scaled_positives'] = similar_games['scaled_positives'].apply(math.log)
        similar_games['scaled_positives'] = scaler.fit_transform(similar_games['scaled_positives'].values.reshape(-1,1))

        similar_games['score'] = similar_games['d2v_similarity']+ 0.26*similar_games['scaled_positives']
        
        similar_games = similar_games.sort_values(by='score',ascending=False)
        return list(similar_games['name'])[:10]

    def load(self):
        self._model = g.Doc2Vec.load(self._path)
