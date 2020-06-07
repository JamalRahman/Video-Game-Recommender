from flask import Flask, request, render_template
from flask_cors import CORS
from flask.views import MethodView

from ml.models import NN, Model, Dummy, EmbeddingsRecommender, TfidfEmbeddingsRecommender

import pandas as pd
import ast, csv, json
import utils


app = Flask(__name__)

CORS(app,resources={r'/*': {'origins': '*'}})

training_data_path = '../data/processed/app_data.csv'
app_data = pd.read_csv(training_data_path)

path_to_model = '../models/doc2vec.pickle'
path_to_cosine_sim = '../models/cosine_sim.pickle'

model = EmbeddingsRecommender(path_to_model,app_data)


with open('../data/processed/app_list.json') as f:
    app_titles = json.load(f)["data"]
    title_list = [item["name"] for item in app_titles]
# Detect if no model exists, set flag

@app.route('/',methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/map',methods=['GET'])
def map():
    return render_template("map.html")

@app.route('/api',methods=['GET'])
def predict():
    if 'input' in request.args:
        model_input = request.args['input']
        model_input = ast.literal_eval(model_input)

        out = model.predict(model_input)
        return {"output": str(out)}
    else:
        return 'Error: No input given'



@app.route('/search',methods=['GET'])
def search():
    if 'query' in request.args:
        query = request.args['query']
        titles = utils.get_superstrings(query,title_list)[:10]
        selected_apps = []
        for app_details in app_titles:
            if app_details['name'] in titles:
                selected_apps.append(app_details);

        return {"apps": selected_apps}
    else:
        return 'Error: No input given'
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')