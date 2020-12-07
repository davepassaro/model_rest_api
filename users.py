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
        #print(token,"tok")
        vered = auxfunctions.verify(token) 
        print(vered)
        if  vered and vered != False:
            content["user_Id"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid(2)"
                }), 401)
        
        new_user = datastore.entity.Entity(key=client.key(constants.users))
        new_user.update({"name":content["name"],"user_Id":content["user_Id"],"boats" : []})
        client.put(new_user)
        return (jsonify({
        "id": new_user.key.id,
        "user_Id": new_user["user_Id"],
        "boats" : [],
        "name":content["name"],
        "self": (request.url + "/" + str(new_user.key.id))
        }), 201)
    elif request.method == "GET":
        query = client.query(kind=constants.users)
        results = list(query.fetch())
        for e in results:
            e["id"] = e.key.id
        return json.dumps(results)
    else:
        return 'Method not recogonized' 
            
@bp.route('/<id>', methods=['DELETE'])

def userDelete(id):
    if request.method == 'DELETE':
        key = client.key(constants.users, int(id))
        user = client.get(key=key)
        if not user:
            return (jsonify({"Error": "No user with this user_id exists"}),404)
        '''query = client.query(kind=constants.boats)
        results = list(query.fetch())
        for e in results:
            #print(e)#["current_boat"])
            if "carrier" in e and e["carrier"] and e["carrier"]["id"] and int(e["carrier"]["id"]) == int(id):
                e["carrier"]["id"] = -1
                e["carrier"]["name"] = ""
                client.put(e)'''
        client.delete(key)
        return ('',204) 

