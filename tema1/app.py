from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from tema import get_random_integer, get_url_by_search, get_image_description, get_metrics
import json

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/<to_search>', methods=['GET'])
def data(to_search):
    IMG_URL = get_url_by_search(to_search)
    IMAGE_DESCRIPTION = get_image_description(IMG_URL).capitalize()

    data_dict = {'IMG_URL': IMG_URL, 'IMAGE_DESCRIPTION': IMAGE_DESCRIPTION}
    return json.dumps(data_dict)


@app.route('/metrics')
def metrics():
    metrics_info = get_metrics()
    return metrics_info


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=8080)
