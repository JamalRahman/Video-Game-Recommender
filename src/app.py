from flask import Flask, request
from flask.views import MethodView

from ml.models import NN, Model, Dummy

app = Flask(__name__)


# Detect if no model exists, set flag

@app.route('/api',methods=['GET','POST'])
def predict():
    if 'input' in request.args:
        model_input = int(request.args['input'])
        return 2*model_input
    else:
        return 'Error: No input given'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')