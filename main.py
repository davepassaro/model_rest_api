
from google.cloud import datastore
from flask import Flask, request, session,render_template,redirect
import json
import constants
import boat
import load
import users
import auxfunctions
from requests_oauthlib import OAuth2Session
from google.auth.transport import requests
import requests
import string
import random
from google.oauth2 import id_token
from google.auth import crypt
from google.auth import jwt
from google.auth.transport import requests
# This disables the requirement to use HTTPS so that you can test locally.
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
client = datastore.Client()
app.register_blueprint(boat.bp)
app.register_blueprint(users.bp)
app.register_blueprint(load.bp)

# These should be copied from an OAuth2 Credential section at
# https://console.cloud.google.com/apis/credentials
client_id = "1034814845689-3gua5nmfjbl17jndavgg4ubjqq77to4f.apps.googleusercontent.com"
client_secret = "73EUBGWnTtZl8Ap3PAIRKiRo"
# This is the page that you will use to decode and collect the info from
# the Google authentication flow
redirect_uri = 'http://localhost:8080/oauth'  # 'https://dave-final-493.wm.r.appspot.com/oauth' #change when deployed*&$%*&$%*&$%*&$%*&$%*&$*&$%

# These let us get basic info to identify a user and not much else
# they are part of the Google People API
scope = ['https://www.googleapis.com/auth/userinfo.profile']
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,
                          scope=scope)


@app.route('/')
def index():
    authorization_url, state = oauth.authorization_url(
        'https://accounts.google.com/o/oauth2/auth',
        # access_type and prompt are Google specific extra
        # parameters.
        access_type="offline", prompt="select_account")
    return 'Please go <a href=%s>here</a> and authorize access.' % authorization_url

# This is where users will be redirected back to and where you can collect
# the JWT for use in future requests
@app.route('/oauth')
def oauthroute():
    token = oauth.fetch_token(
        'https://accounts.google.com/o/oauth2/token',
        authorization_response=request.url,
        client_secret=client_secret)
    req = requests.Request()

    id_info = id_token.verify_oauth2_token( 
    token['id_token'], req, client_id)
    #id = auxfunctions.verify(token)
    #tokenStr = token['id_token']
    x=' '
    return "Your JWT is: "+ token['id_token'] + ' <br><br><br>' + 'and your id (sub value) is ' + id_info["sub"]



@app.route('/owner/<id>/boats', methods=['GET'])
def owner(id):
    if request.method == "GET":
        query = client.query(kind=constants.boats)
        results = list(query.fetch())
        getList = []
        for e in results:
            if "owner" in e and e["owner"] == id:
                if "public" in e and e["public"] == True:
                    getList.append(e)
        return (json.dumps(getList),200)
# This page demonstrates verifying a JWT. id_info['email'] contains
# the user's email address and can be used to identify them
# this is the code that could prefix any API call that needs to be
# tied to a specific user by checking that the email in the verified
# JWT matches the email associated to the resource being accessed.
@app.route('/verify-jwt')
def verify():
    req = requests.Request()

    id_info = id_token.verify_oauth2_token( 
    request.args['jwt'], req, client_id)

    return repr(id_info) + "<br><br> the user is: " + id_info['email']
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


