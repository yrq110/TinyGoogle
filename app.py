from flask import Flask, request
import json
from bson import json_util
import requests
app = Flask(__name__)
#
# print json_data['queries']['request'][0]['count']


def toJson(data):
    line = json.dumps(data, default=json_util.default)
    return line

@app.route('/', methods=['GET'])
def detail_json():
    url = "https://www.googleapis.com/customsearch/v1"
    querystring = {"key":"AIzaSyCieQLOf0-4RILST4Eivz7CjdOp-4cCUOE","cx":"009989704776709960942:xgqpl9qptva","num":"10","q":"python"}
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

if __name__ == '__main__':
    app.run(debug = True)
