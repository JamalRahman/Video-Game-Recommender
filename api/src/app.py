from flask import Flask, request
from flask_cors import CORS

from flask.views import MethodView

from ml.models import NN, Model, Dummy, EmbeddingsRecommender

import pandas as pd
import ast, csv
import utils


app = Flask(__name__)

CORS(app,resources={r'/*': {'origins': '*'}})

training_data_path = '../data/processed/app_data.csv'
app_data = pd.read_csv(training_data_path)

path_to_model = '../models/doc2vec.pickle'
model = EmbeddingsRecommender(path_to_model,app_data)

with open('../data/processed/app_list.csv') as f:
    title_list = [line.rstrip() for line in f]
# Detect if no model exists, set flag

@app.route('/api',methods=['GET','POST'])
def predict():
    if 'input' in request.args:
        model_input = request.args['input']
        model_input = ast.literal_eval(model_input)

        out = model.predict(model_input)
        return {"output": str(out)}
    else:
        return 'Error: No input given'

@app.route('/search',methods=['GET','POST'])
def search():
    query = request.args['query']
    titles = utils.get_superstrings(query,title_list)

    return {"titles": titles}
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')