from flask import Flask
from ml.models import NN, Model

app = Flask(__name__)

@app.route('/')
def index():
    return 'yeet'

if __name__ == '__main__':
    app.run(host='0.0.0.0')