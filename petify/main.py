import os
import json
import requests

from flask import Flask, request, redirect
# from flask_cors import CORS

from database.db import DbHandler
from models.Advert import Advert
from scripts.add_event import add_event
from scripts.send_email import send_email
from blobs.blb import BlobStorage

app = Flask(__name__)
# app.secret_key = os.urandom(24)
# CORS(app)

db_credentials = json.load(open(os.path.join(os.path.dirname(__file__), 'configs/db_credentials.json')))
db = DbHandler(db_credentials)

with open(os.path.join(os.path.dirname(__file__), 'configs/calendar_secret.json')) as f:
    calendar_secret = json.load(f)
credentials = (calendar_secret['CLIENT_ID'], calendar_secret['CLIENT_SECRET'])

blob_credentials = json.load(open('./configs/blob_credentials.json'))
blob = BlobStorage()


state = None
calendar_advert_id = None


@app.route('/')
def hello_world():
    return 'Hey its Python Flask application!'


@app.route('/send_email', methods=['POST'])
def send_mail():
    print(request.get_json())
    body = request.get_json()
    advert = db.get_advert_by_id(body['id'])
    send_email(body['to'], body['username'], advert)
    return 'Sent mail'


@app.route('/add_event/<id>')
def add_event(id):
    try:
        from scripts.gcalendar import add_event_gcalendar
        advert = db.get_advert_by_id(id)
        add_event_gcalendar(advert)

        return 'Event added'
    except Exception as err:
        print(err.with_traceback(None))
        return 'Event failed', 500

######
from oauthlib.oauth2 import WebApplicationClient

config = json.load(open("config/config.json"))
GOOGLE_CLIENT_ID = config["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = config["GOOGLE_CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)

@app.route('/login')
def login():
    authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"

    request_uri = client.prepare_request_uri(authorization_endpoint, redirect_uri=request.base_url.replace('http', 'https').replace('httpss', 'https') + "/callback",
                                             scope=["https://www.googleapis.com/auth/calendar"])
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    try:
        import pickle
        token_endpoint = "https://oauth2.googleapis.com/token"

        token_url, headers, body = client.prepare_token_request(token_endpoint, authorization_response=request.url.replace('http', 'https').replace('httpss', 'https'),
                                                                redirect_url=request.base_url.replace('http', 'https').replace('httpss', 'https'), code=code)
        token = requests.post(token_url, headers=headers, data=body, auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)).json()

        with open('token.pickle', 'wb') as f:
            pickle.dump(token, f)

        return 'OK'
    except Exception as e:
        print(e)
        return e
######

# @app.route('/add_event/', methods=['GET'])
# def auth_step_one(id):
#     global state
#     scopes = ['Calendars.ReadWrite']
#
#     callback = request.url_root + 'add_event/callback'
#
#     if callback.startswith('http://'):
#         callback = callback.replace('http://', 'https://', 1)
#
#     app.logger.error(f"Callback auth step one: {callback}")
#
#     account = Account(credentials)
#
#     if not account.is_authenticated:
#         global calendar_advert_id
#         url, state = account.con.get_authorization_url(requested_scopes=scopes, redirect_uri=callback)
#         calendar_advert_id = id
#     else:
#         advert = db.get_advert_by_id(id)
#         add_event(account, advert)
#         return 'Event added'
#
#     if url.startswith('http://'):
#         url = url.replace('http://', 'https://', 1)
#
#     app.logger.error("Finished auth step one")
#     # app.logger.error("Redirect url:", url)
#
#     return redirect(url)
#
#
# @app.route('/add_event/callback')
# def auth_step_two_callback():
#     global state
#     account = Account(credentials)
#
#     url = request.url
#     callback = request.base_url
#
#     if callback.startswith('http://'):
#         callback = callback.replace('http://', 'https://', 1)
#
#     app.logger.error(f"Callback auth step two: {callback}")
#
#     if url.startswith('http://'):
#         url = url.replace('http://', 'https://', 1)
#
#     app.logger.error(f"Token Url auth step two: {url}")
#
#     result = account.con.request_token(url, state=state, redirect_uri=callback, store_token=False)
#
#     app.logger.error("Finished auth step two")
#
#     if result:
#         global calendar_advert_id
#         advert = db.get_advert_by_id(calendar_advert_id)
#         add_event(account, advert)
#         return 'Event added'
#     return 'Failed'

@app.route('/upload-image', methods=['POST'])
def upload_image():
    # GET at https://petifystorage.blob.core.windows.net/petifyblob/{advert_id}.png
    body = request.get_json()
    advert_id = body['advertId']
    image_data = body['imageData']
    blob.upload(advert_id, image_data)
    return ''


@app.route('/add_user', methods=['POST'])
def add_user():
    user_doc = request.get_json()
    if not db.user_already_exists(user_doc):
        db.add_user(user_doc)

    return ''


@app.route('/advert', methods=['POST'])
def add_advert():
    body = request.get_json()
    # TODO: Check body
    new_advert = Advert(**body)
    new_advert.availability = True
    db.add_advert(new_advert)
    return json.dumps({"advert_id": new_advert.id})


@app.route('/adverts')
def get_adverts():
    adverts = db.get_adverts()
    return json.dumps([adv.to_dict() for adv in adverts])


@app.route('/adverts/<id>')
def get_user_adverts(id):
    user_adverts = db.get_user_adverts(id)
    return json.dumps([adv.to_dict() for adv in user_adverts])


@app.route('/subscriptions/<id>')
def get_user_subscriptions(id):
    subs = db.get_user_subscriptions(id)
    return json.dumps([adv.to_dict() for adv in subs])


@app.route('/subscribe', methods=['POST'])
def subscribe():
    body = request.get_json()
    user_id = body['user_id']
    advert_id = body['advert_id']
    db.subscribe_user_to_advert(user_id, advert_id)

    advert = db.get_advert_by_id(body['advert_id'])

    data = {"to": body['user_id'],
            "username": advert.user_name,
            "description": advert.description,
            "start_date": advert.start_date,
            "price": f'{advert.price} RON'}

    requests.get('https://petifyfunction.azurewebsites.net/api/my-func', data=json.dumps(data))
    requests.get(f'{request.url_root}add_event/{advert_id}', verify=False)

    return json.dumps({"response": "Subscribe"})


@app.route('/advert/<id>', methods=['GET', 'PATCH'])
def advert_by_id(id):
    if request.method == 'GET':
        try:
            advert = db.get_advert_by_id(id)
            return json.dumps(advert.to_dict())
        except:
            return 'Advert not found', 404
    elif request.method == 'PATCH':
        # TODO
        return 'Method not implemented', 501
    else:
        return '', 404

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
