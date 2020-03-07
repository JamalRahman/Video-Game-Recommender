from flask import Flask
from ml.models import CNN

app = Flask(__name__)


@app.route('/')
def index():
    model = CNN()
    model.load()
    return 'yeet'

if __name__ == '__main__':
    app.run(host='0.0.0.0')