
from flask import Blueprint, request, jsonify
from google.cloud import datastore
import json
import constants

client = datastore.Client()

bp = Blueprint('load', __name__, url_prefix='/loads')

@bp.route('', methods=['POST','GET'])
def loads_get_post():
    if request.method == 'POST':
        content = request.get_json()
        if not content or "carrier" not in content or "content" not in content or "delivery_date" not in content or "weight" not in content:
            return (jsonify({"Error": "The request object is missing at least one of the required attributes"}),400)        
        new_load = datastore.entity.Entity(key=client.key(constants.loads))
        new_load.update({"carrier": content["carrier"], "content": content["content"],"weight": content["weight"],"delivery_date": content["delivery_date"]})
        client.put(new_load)
        new_load["id"] = new_load.key.id
        new_load["self"] = request.url + '/' + str(new_load.key.id)
        return (json.dumps(new_load),201)
    elif request.method == 'GET':
        query = client.query(kind=constants.loads)
        q_limit = int(request.args.get('limit', '5'))
        q_offset = int(request.args.get('offset', '0'))
        g_iterator = query.fetch(limit= q_limit, offset=q_offset)
        pages = g_iterator.pages
        results = list(next(pages))
        if g_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
        else:
            next_url = None
        for e in results:
            e["id"] = e.key.id
        output = {"loads": results}
        if next_url:
            output["next"] = next_url
        return json.dumps(output)
    else:
        return ('Method not recogonized')
'''        
query = client.query(kind=constants.loads)
        results = list(query.fetch())
        for e in results:
            e["id"] = e.key.id
            e["self"] = str(request.url)+'/'+str(e.key.id)
        return json.dumps(results)
    else:
        return 'Method not recogonized'
'''




@bp.route('/del', methods=['GET','DELETE'])
def del_loads():
    if request.method == 'DELETE':
        query = client.query(kind=constants.boats)
        results = list(query.fetch())
        print (results,"\n\n\n\n")
        return ('',200)

@bp.route('/<id>', methods=['GET','DELETE','PUT','PATCH'])
def loads_put_delete(id):
    if request.method == 'DELETE':
        load_key = client.key(constants.loads, int(id))
        load = client.get(key=load_key)

        if not load:
            return (jsonify({"Error": "No load with this load_id exists"}),404)
        query = client.query(kind=constants.boats)
        results = list(query.fetch())
        print((load,"    "))
        i=0
        if ( (load["carrier"] == None) or load["carrier"]["id"] == -1):
            client.delete(load_key)
            return ('',204)
        else:  #delete the load from the owner boat
            for boat in results:
                #print("\n\nboat  ",boat,"\n\n")
                #print (e)#, "          ",load["carrier"]["id"])
                #if int(boat.key.id) == load.key.id:
                    #print(e)#["current_boat"])
                if "loads" in boat and boat["loads"]:
                    for i in boat["loads"]:
                        print("\ni     ",i)#,"    load   ",load)
                        if "id" in i and i["id"] == id or i == id:
                            print(boat)
                            boat["loads"].remove(i)
                            print(boat)
                            client.put(boat)
                            print("magic\n\n\n",i)
                            client.delete(load_key)
                            return ('',204)

        return('',404)

    elif request.method == 'GET':
        content = request.get_json()
        load_key = client.key(constants.loads, int(id))
        load= client.get(key=load_key)
        if not load:
            return (jsonify({"Error": "No load with this load_id exists"}),404)
            #print("here1",boat["loads"])
            #print("\n\nl",l,"\nl[id]",l["id"])
        strToAdd = str(load["carrier"]["id"])
        load["carrier"]["self"] = request.url_root+"boats/"+strToAdd
        #print(load)
        load["self"] = str(request.url)
        load["id"] = load.key.id
        return (json.dumps(load))
    elif request.method == 'PUT':
        content = request.get_json()
        load_key = client.key(constants.loads, int(id))
        load = client.get(key=load_key)
        if not load:
            return (jsonify({"Error": "No load with this boat_id exists"}),404)
        if not content or "carrier" not in content or "content" not in content or "delivery_date" not in content or "weight" not in content:
            return (jsonify({"Error": "The request object is missing at least one of the required attributes"}),400)  
        load.update({"carrier": content["carrier"], "content": content["content"],"weight": content["weight"],"delivery_date": content["delivery_date"]})
        client.put(load)
        load["id"] = load.key.id
        load["self"] = request.url  # + '/' + str(boat.key.id)
        return (jsonify({
        "id": load.key.id,
        "carrier": content["carrier"],
        "content": content["content"],
        "weight": content["weight"],
        "delivery_date": content["delivery_date"],
        "self": (request.url)# + "/" + str(boat.key.id))
        }), 200)
    elif request.method == 'PATCH':
        content = request.get_json()
        load_key = client.key(constants.loads, int(id))
        load = client.get(key=load_key)
        if not load:
            return (jsonify({"Error": "No load with this boat_id exists"}),404)
        if not content or "carrier" not in content or "content" not in content or "delivery_date" not in content or "weight" not in content:
            return (jsonify({"Error": "The request object is missing at least one of the required attributes"}),400)  
        load.update({"carrier": content["carrier"], "content": content["content"],"weight": content["weight"],"delivery_date": content["delivery_date"]})
        client.put(load)
        load["id"] = load.key.id
        load["self"] = request.url  # + '/' + str(boat.key.id)
        return (jsonify({
        "id": load.key.id,
        "carrier": content["carrier"],
        "content": content["content"],
        "weight": content["weight"],
        "delivery_date": content["delivery_date"],
        "self": (request.url)# + "/" + str(boat.key.id))
        }), 200)
    else:
        return jsonify('Method not recogonized',400)



