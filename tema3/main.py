import json
import os

import requests
from flask import Flask, render_template, redirect, request, url_for
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
from datetime import datetime
from webapp.scripts.send_email import send_welcome_message
from webapp.scripts.gcalendar import add_event
from webapp.models.User import User
from webapp.models.Advert import Advert
from webapp.db.DbHandler import DbHandler

try:
  import googleclouddebugger
  googleclouddebugger.enable()
except ImportError:
  pass


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)

config = json.load(open("config/config.json"))
GOOGLE_CLIENT_ID = config["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = config["GOOGLE_CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_CLOUD_FUNCTION_URL = "https://europe-west2-cloudcomputing-272912.cloudfunctions.net/hello_user"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(os.path.dirname(__file__),
                                                            r"config/firestore_credentials.json")
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client = WebApplicationClient(GOOGLE_CLIENT_ID)
db = DbHandler(None)


@login_manager.user_loader
def load_user(user_id):
    db_user = db.get_user_by_id()
    db_user['id'] = user_id
    return User.from_dict(db_user)


@app.route('/')
def index():
    if current_user.is_authenticated:
        # test('cloudcomputing-272611@appspot.gserviceaccount.com', current_user.getEmail())
        username = current_user.getUsername()
        welcome_message = get_welcoome_message(username)
        # send_welcome_message('cloudcomputingteamfii@gmail.com', current_user.getEmail(), current_user.getUsername())
        adverts = db.get_adverts()
        return render_template('index.html', user=True, welcome_message= welcome_message, adverts=adverts)
    else:
        return render_template('login.html', user=False)

# @app.route('/database')
# def database():
#     from datetime import datetime
#     advert1 = Advert('5Rz5xP4wyh7DGr88L37p')
#     advert2 = Advert('DiNoO7ovklVcjHRr9HrC')
#     advert3 = Advert('EnaSqf9H9uGWXaF3n6xc')
#     advert4 = Advert('hvnryB1eNVHhl80B7zDa')
#     advert5 = Advert('o46lvkuQZ8nchQ56fPF6')
#     db.delete_advert(advert1)
#     db.delete_advert(advert2)
#     db.delete_advert(advert3)
#     db.delete_advert(advert4)
#     db.delete_advert(advert5)


# @app.route('/database')
# def database():
#     from datetime import datetime
#     advert = Advert(user_id='412341242', title='Test title', image='Test image', description='Test description', date=datetime.now(), duration=40, location='Iasi, Romania', price=10, availability=True)
#     advert2 = Advert(user_id='412341241241', title='Test title2', image='Test1 image', description='Test description2', date=datetime.now(), duration=20, location='Iasi, Romania', price=30, availability=False)

#     db.add_advert(advert)
#     db.add_advert(advert2)

#     add_event(advert)
#     add_event(advert2)

#     print(db.get_adverts())


# @app.route('/account')
# def account():
#     pass


@app.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(authorization_endpoint, redirect_uri=request.base_url.replace('http', 'https').replace('httpss', 'https') + "/callback",
                                             scope=["openid", "email", "profile",
                                                    "https://www.googleapis.com/auth/calendar"])
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")

    try:
        import pickle
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = client.prepare_token_request(token_endpoint, authorization_response=request.url.replace('http', 'https').replace('httpss', 'https'),
                                                                redirect_url=request.base_url.replace('http', 'https').replace('httpss', 'https'), code=code)
        token = requests.post(token_url, headers=headers, data=body, auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)).json()

        with open('token.pickle', 'wb') as f:
            pickle.dump(token, f)

        client.parse_request_body_response(json.dumps(token))
        user_info_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(user_info_endpoint)
        user_info_response = requests.get(uri, headers=headers, data=body)

        unique_id = user_info_response.json()["sub"]
        users_email = user_info_response.json()["email"]
        users_name = user_info_response.json()["given_name"]

        user = User(id=unique_id, username=users_name, email=users_email)
        db.user = user

        if not db.get_user_by_id():
            db.add_user()

        login_user(db.user)
        return redirect(url_for("index"))
    except Exception as e:
        print(e)
        return e


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/display-advert", methods=['GET'])
def displayFormAdvert():
    return render_template('add-advert.html')

@app.route("/api/add-advert", methods=['POST'])
def addAdvert():
    body = request.get_json()
    datetime_string = body['date']
    fmt = "%Y-%m-%dT%H:%M"
    adv_date = datetime.strptime(datetime_string, fmt)
    req_object = {
        'title': body['title'],
        'description': body['description'],
        'price': int(body['price']),
        'duration': int(body['duration']),
        'availability': True,
        'date': adv_date,
        'image': 'Img title default',
        'location': 'Iasi'
    }
    print(req_object)
    advert = Advert(**req_object)
    db.add_advert(advert)
    return ''

@app.route("/api/add-event", methods=['POST'])
def addEvent():
    body = request.get_json()
    advert_id = body['advertId']
    advert = db.get_advert_by_id(advert_id)
    add_event(advert)
    advert.availability = False
    db.edit_advert(advert)
    return ''

def get_google_provider_cfg():
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except requests.RequestException as e:
        print('Google API request failed')
        print(e)

def is_user(user):
    print(type(user))
    return isinstance(user, User)

def get_welcoome_message(username):
    try:
        url = GOOGLE_CLOUD_FUNCTION_URL + '?username=' + username
        msg = requests.get(url)
        print(msg.text)
        return msg.text
    except requests.RequestException as e:
        print('Google API request failed')
        print(e)
        return ''

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, ssl_context='adhoc')
