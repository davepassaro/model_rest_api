from google.cloud import datastore
from flask import Flask, request
from requests_oauthlib import OAuth2Session
import json
from google.oauth2 import id_token
from google.auth import crypt
from google.auth import jwt
from google.auth.transport import requests
client_id = "1034814845689-3gua5nmfjbl17jndavgg4ubjqq77to4f.apps.googleusercontent.com"
client_secret = "73EUBGWnTtZl8Ap3PAIRKiRo"
def verify(jwtok):
    req = requests.Request()
    #print(jwtok,"jwt") 
    try: 
        id_info = id_token.verify_oauth2_token(jwtok, req, client_id)
        #print(id_info)
    except :

       return False
    #print(id_info,"idfo")
    if  id_info and "iss" in id_info and id_info['iss'] != 'accounts.google.com':
        return False
        #  cited google auth docs
    else:
        return id_info["sub"]

    
