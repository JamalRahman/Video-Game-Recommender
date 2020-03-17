from flask import Flask
from ml.models import CNN, Model

app = Flask(__name__)


@app.route('/')
def index():
    model = CNN('models/1/')
    return 'yeet'

if __name__ == '__main__':
    app.run(host='0.0.0.0')