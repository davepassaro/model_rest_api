from google.cloud import datastore
from flask import Flask, Blueprint, request,jsonify
import json
import constants
import auxfunctions

client = datastore.Client()
bp = Blueprint('boat' ,__name__, url_prefix='/boats')

@bp.route('', methods=['POST','GET'])
def boats_get_post():
    if request.method == 'POST':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify({"Error": "Media Type unsupported"}),406)
        content = request.get_json()
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        vered = auxfunctions.verify(token) 
        #print(vered)
        if  vered and vered != False:
            content["owner"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        if(len(content) != 4):
            return (jsonify({
                "Error": "The request object is missing at least one of the required attributes"
                }), 400)
        new_boat = datastore.entity.Entity(key=client.key(constants.boats))
        new_boat.update({"name": content["name"],"owner":content["owner"], "type": content["type"],
          "length": content["length"],"loads" : []})
        client.put(new_boat)
        return (jsonify({
        "id": new_boat.key.id,
        "name": content["name"],
        "owner":content["owner"],
        "type": content["type"],
        "length": content["length"],
        "loads" : [],
        "self": (request.url + "/" + str(new_boat.key.id))
        }), 201)
    elif request.method == 'GET':
        #print(query)
        #getList = []
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify({"Error": "Media Type unsupported"}),406)
        content = {}
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)

        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        vered = auxfunctions.verify(token) 
        #print(vered)
        if  vered and vered != False:
            content["owner"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        query = client.query(kind=constants.boats)
        query = query.add_filter('owner', '=', (content["owner"]))
        resultsTotal = list(query.fetch()) 
        lenResults = len(resultsTotal)
        q_limit = int(request.args.get('limit', '5'))
        q_offset = int(request.args.get('offset', '0'))
        l_iterator = query.fetch(limit= q_limit, offset=q_offset)
        pages = l_iterator.pages
        results = list(next(pages))
        if l_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
        else:
            next_url = None
        for e in results:
            e["id"] = e.key.id
            e["self"] = (request.url +'/'+ str(e.key.id))
        output = {"boats": results,"usersTotalBoats":lenResults}
        if next_url:
            output["next"] = next_url
        return json.dumps(output)
    else:
        return jsonify('Method not recogonized',400)

#  results = list(query.fetch())
#        for e in results:
#            e["id"] = e.key.id
#        return json.dumps(results)
#    else:
#        return 'Method not recogonized'  






@bp.route('/<id>', methods=['PUT','PATCH','DELETE','GET'])
def boats_patch_delete(id):
    if request.method == 'PUT':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify({"Error": "Media Type unsupported"}),406)
        content = request.get_json()
        if  "name" not in  content or "type"  not in content or "length" not in content:# or not request.body:#and content:
            return (jsonify({"Error": "The request object is missing at least one of the required attributes"}),400)
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        vered = auxfunctions.verify(token) 
        #print(vered)
        if  vered and vered != False:
            content["owner"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        if content["owner"] != boat["owner"]:
            return(jsonify({"Error": "User is not permitted to access this resource."},401))
        if not boat:
            return (jsonify({"Error": "No boat with this boat_id exists"}),404)
        boat.update({"name": content["name"], "type": content["type"],
          "length": content["length"]})
        client.put(boat)
        boat["id"] = boat.key.id
        boat["self"] = request.url  # + '/' + str(boat.key.id)
        return (jsonify({
        "id": boat.key.id,
        "name": boat["name"],
        "type": boat["type"],
        "length": boat["length"],
        "owner" : boat["owner"],
        "self": (request.url)# + "/" + str(boat.key.id))
        }), 200)
    elif request.method == 'PATCH':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify({"Error": "Media Type unsupported"}),406)
        content = request.get_json()
        if  len(content) < 1:# or not request.body:#and content:
            return (jsonify({"Error": "The request object is missing at least one of the required attributes"}),400)
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        vered = auxfunctions.verify(token) 
        #print(vered)
        if  vered and vered != False:
            content["owner"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        if not boat:
            return (jsonify({"Error": "No boat with this boat_id exists"}),404)
        if content["owner"] != boat["owner"]:
            return(jsonify({"Error": "User is not permitted to access this resource."},401))
        print(content["owner"],boat["owner"])
        if "name" in content and content["name"]:
            boat.update({"name": content["name"]})
        if "type" in content and content["type"]:
            boat.update({"type": content["type"]})
        if "length" in content and content["length"]:
            boat.update({"length":content["length"]})
        client.put(boat)
        boat["id"] = boat.key.id
        boat["self"] = request.url  # + '/' + str(boat.key.id)
        return (jsonify({
        "id": boat.key.id,
        "name": boat["name"],
        "type": boat["type"],
        "length": boat["length"],
        "owner" : boat["owner"],
        "self": (request.url)# + "/" + str(boat.key.id))
        }), 200)
    elif request.method == 'DELETE':
        if not id:
            return (jsonify({"Error": "No boat id provided"}),404)
        key = client.key(constants.boats, int(id))
        boat = client.get(key=key)
        if not boat:
            return (jsonify({"Error": "No boat with this boat_id exists"}),404)

        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        vered = auxfunctions.verify(token) 
        #print(vered)
        if  vered and vered == False:
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        if vered != boat["owner"]:
            return(jsonify({"Error": "User is not permitted to access this resource."},401))
        query = client.query(kind=constants.loads)
        results = list(query.fetch())
        for e in results:
            #print(e)#["current_boat"])
            if "carrier" in e and e["carrier"] and e["carrier"]["id"] and int(e["carrier"]["id"]) == int(id):
                e["carrier"]["id"] = -1
                e["carrier"]["name"] = ""
                client.put(e)
        client.delete(key)
        return ('',204)
    elif request.method == 'GET':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify({"Error": "Media Type unsupported"}),406)
        #print("url      ",request.url)
        content ={}
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        vered = auxfunctions.verify(token) 
        print(vered)
        if  vered and vered != False:
            content["owner"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        x = 0
        if boat:
            if boat["owner"] == content["owner"]:
                #print("here1",boat["loads"])
                for l in boat["loads"]:  #FOR DICTS IN LIST
                    #print("\n\nl",l,"\nl[id]",l["id"])
                    strToAdd = str(l["id"])
                    l["self"] = request.url_root+"loads/"+strToAdd
                #print(boat)
                return (jsonify({
            "id": boat.key.id,
            "name": boat["name"],
            "type": boat["type"],
            "length": boat["length"],
            "owner" : boat["owner"],
            "loads":boat["loads"],
            "self": (request.url )#+ "/" + str(boat.key.id))
            }))
            else:
                return(jsonify({"Error": "User is not permitted to access this resource."},401))
        else:
            return (jsonify({"Error": "No boat with this boat_id exists"}),404)
    else:
        return jsonify('Method not recogonized',400)






@bp.route('/<idBoat>/loads/<idLoad>', methods=['PUT','DELETE'])
def add_remove_Loads(idLoad,idBoat):
    if request.method == 'PUT':
        content = request.get_json()
        print(content)
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        vered = auxfunctions.verify(token) 
        content={}
        if  vered and vered != False:
            content["owner"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)

        boat_key = client.key(constants.boats, int(idBoat))
        boat= client.get(key=boat_key)
        if not boat:# or boat["loads"][0] == idLoad:
            return (jsonify({"Error":  'The specified boat and/or load does not exist'}),404)
        print(vered,boat)
        
        if vered != boat["owner"]:
            return(jsonify({"Error": "User is not permitted to access this resource."},401))
        load_key = client.key(constants.loads, int(idLoad))
        load = client.get(key=load_key)
        print(load,"here")
        if not load:# or boat.key.id != slip["current_boat"]:
            return (jsonify({"Error":  'The specified boat and/or load does not exist'}),404)
        for k in boat["loads"]:
            if k["id"] == idLoad:
                return (jsonify({"Error": "The boat already contains this load"}),403) 
        #if load["current_boat"] != None:
        #    return (jsonify({"Error": "The slip is not empty"}),403) 
        load.update({"carrier" :{"id": int(idBoat),"name":boat["name"]}})
        #,{"self",request.url_root+str(idBoat)}}})
        #boat.update({"loads":{"id":int(idLoad)}})
        boat["loads"].append({"id":idLoad,"delivery_date":load["delivery_date"],"content":load["content"],"weight":load["weight"]})
        client.put(load)
        client.put(boat)
        #print ("\n\n",boat,"\n\n",load,"\n\n")

        return ('',204)
    if request.method == 'DELETE':
        content = request.get_json()
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        if bearer == None: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)
        token = bearer.split()[1]  # YourTokenHere cited stack overflowhttps://stackoverflow.com/questions/63518441/how-to-read-a-bearer-token-from-postman-into-python-code
        vered = auxfunctions.verify(token) 
        content={}
        if  vered and vered != False:
            content["owner"] =vered
        else: 
            return (jsonify({
                "Error": "The request token was missing or invalid"
                }), 401)

        load_key = client.key(constants.loads, int(idLoad))
        load = client.get(key=load_key)
        boat_key = client.key(constants.boats, int(idBoat))
        boat = client.get(key=boat_key)
        if vered != boat["owner"]:
            return(jsonify({"Error": "User is not permitted to access this resource."},401))
        #print("boat ",boat)
        #print("load   ",load)

        #print("here")
        #print(slip["current_boat"] , "here == ", idBoat)
        if not load or not boat or   int(load["carrier"]["id"]) != int(idBoat):
            return (jsonify({"Error":  'No load with this load_id is at the boat with this boat_id'}),404)
        load.update({ "carrier": {"id":-1,"name":""}})
        for i in boat["loads"]:
            if i["id"] == idLoad:
                boat["loads"].remove(i)
        #print("boat ",boat)
        #print("load   ",load)
        client.put(load)
        client.put(boat)
        return ('',204)
        
        




        
@bp.route('/<idBoat>/loads', methods=['GET'])#,'DELETE'])
def get_Loads(idBoat):
    if request.method == 'GET':
        content = request.get_json()
        print("content",content)
        boat_key = client.key(constants.boats, int(idBoat))
        boat= client.get(key=boat_key)
        #print ("             \n\n",boat,"\n\n\n")
        if not boat:# or boat["loads"][0] == idLoad:
            return (jsonify({"Error":  'The specified boat and/or load does not exist'}),404)
        for l in boat["loads"]:  #FOR DICTS IN LIST
        #print("\n\nl",l,"\nl[id]",l["id"])
            strToAdd = str(l["id"])
            l["self"] = request.url_root+"loads/"+strToAdd
        return (json.dumps(boat),200)        
    else:
        return jsonify("Method not found",400)