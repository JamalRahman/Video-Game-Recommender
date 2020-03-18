from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from ml.models import NN, Model

app = Flask(__name__)
api = Api(app)

# Detect if no model exists, set flag

class _ModelCaller(Resource):
    
    def get(self):
        return self.post()
    
    def post(self):
        return {'prediction':1}


api.add_resource(_ModelCaller, '/api')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')