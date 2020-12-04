from google.cloud import datastore
from flask import Flask, Blueprint, request,jsonify
import json
import constants
import boat
import load
import users
import auxfunctions
client = datastore.Client()
bp = Blueprint('users' ,__name__, url_prefix='/users')



@bp.route('', methods=['POST','GET'])
def users_get_post():
    if request.method == 'POST':
        content = request.get_json()
        headers = request.headers
        if(len(content) < 1):
            return (jsonify({
                "Error": "The request object is missing at least one of the required attributes"
                }), 400)
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid(1)"
                }), 401)
        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        print(token,"tok")
        vered = auxfunctions.verify(token) 
        print(vered)
        if  vered and vered != False:
            content["user_id"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid(2)"
                }), 401)
        
        new_user = datastore.entity.Entity(key=client.key(constants.users))
        new_user.update({"name":content["name"],"user_id":content["user_id"],"boats" : []})
        client.put(new_user)
        return (jsonify({
        "id": new_user.key.id,
        "user_id": new_user["user_id"],
        "boats" : [],
        "name":content["name"],
        "self": (request.url + "/" + str(new_user.key.id))
        }), 201)
    elif request.method == "GET":
        