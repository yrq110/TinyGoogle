from flask import Flask, request
import json, sys
from bson import json_util
from bson.objectid import ObjectId
import pymongo
from urllib import unquote
import requests
app = Flask(__name__)
mongoClient = pymongo.MongoClient("mongodb://yrq110:room506@ds011298.mongolab.com:11298/house_fs")
db = mongoClient['house_fs']

url = "https://www.googleapis.com/customsearch/v1"

querystring = {"key":"AIzaSyCieQLOf0-4RILST4Eivz7CjdOp-4cCUOE","cx":"009989704776709960942:xgqpl9qptva","num":"10","q":"python"}

# headers = {
#     'cache-control': "no-cache",
#     'postman-token': "056e7561-cd3d-fa25-9ed2-aabd3b349410"
#     }

response = requests.request("GET", url, params=querystring)

json_data = json.loads(response.text)

print json_data['queries']['request'][0]['count']


def toJson(data):
    line = json.dumps(data, default=json_util.default)
    return line

@app.route('/detail/', methods=['GET'])
def detail_json():
    url = "https://www.googleapis.com/customsearch/v1"

    querystring = {"key":"AIzaSyCieQLOf0-4RILST4Eivz7CjdOp-4cCUOE","cx":"009989704776709960942:xgqpl9qptva","num":"10","q":"python"}

    # headers = {
    #     'cache-control': "no-cache",
    #     'postman-token': "056e7561-cd3d-fa25-9ed2-aabd3b349410"
    #     }

    response = requests.request("GET", url, params=querystring)

    json_data = json.loads(response.text)
    print type(json_data)
    return toJson(response.text)
    # print(response.text)
    # if request.method == 'GET':
    #     results = db['house_detail'].find().limit(10)
    #     json_results= []
    #     for result in results:
    #         json_results.append(result)
    #     return toJson(json_results)

@app.route('/list/', methods=['GET'])
def list_json():
    if request.method == 'GET':
        count = request.args.get('count')
        times = request.args.get('times')
        skip_count = int(times)*int(count)
        #results = db['house_list'].find().skip(skip_count).limit(int(count))
        results = db['house_detail'].find().skip(skip_count).limit(int(count))
        list_results = []
        for result in results:
            list_results.append(result)
        return toJson(list_results)

@app.route('/sortU/', methods=['GET'])
def sortU_json():
    if request.method == 'GET':
        results = db['house_list'].find().sort([("price",1)])
        #results = db['house_list'].find({'price':{"$exists":true}},{'price':1})
        json_results= []
        for result in results:
            json_results.append(result)
        return toJson(json_results)

@app.route('/sortD/', methods=['GET'])
def sortD_json():
    if request.method == 'GET':
        results = db['house_list'].find().sort([("price",-1)])
        #results = db['house_list'].find({'price':{"$exists":true}},{'price':1})
        json_results= []
        for result in results:
            json_results.append(result)
        return toJson(json_results)

@app.route('/find/', methods=['GET'])
def find_json():
    if request.method == 'GET':
        results = db['house_list'].find({'price':{'$lt':5000}}).sort([('price',-1)])
        #results = db['house_list'].find({'price':{"$exists":true}},{'price':1})
        json_results= []
        for result in results:
            json_results.append(result)
        return toJson(json_results)


#@app.route('/hello/<address>',methods=['GET'])
@app.route('/hello/',methods=['GET'])
def detail_search_json():
    if request.method == 'GET':
        room = request.args.get('room')
        room = unquote(room)
        #results = db['house_list'].find({'address':{'$regex':address}}).limit(10)

        price = request.args.get('price')
        price = unquote(price)
        #results = db['house_list'].find({'address':{'$regex':address}}).limit(10)
        results = db['house_detail'].find({'house_type':{'$regex':room},'price_detail':{'$regex':price}}).limit(10)
        json_results= []
        for result in results:
            json_results.append(result)
        return toJson(json_results)

@app.route('/tes/',methods=['GET'])
def test_json():
    if request.method == 'GET':
        results = db['house_detail'].find({'publish_time':'2016-02-03','price_detail':'3000'})
        json_results= []
        for result in results:
            json_results.append(result)
        return toJson(json_results)
if __name__ == '__main__':
    app.run(debug = True)
