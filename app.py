from flask import Flask, request
import json, sys
import requests
app = Flask(__name__)

# print json_data['queries']['request'][0]['count']


def toJson(data):
    line = json.dumps(data)
    return line

@app.route('/', methods=['GET'])
def detail_json():
    url = "https://www.googleapis.com/customsearch/v1"
    querystring = {"key":"AIzaSyCieQLOf0-4RILST4Eivz7CjdOp-4cCUOE","cx":"009989704776709960942:xgqpl9qptva","num":"10","q":"python"}
    response = requests.request("GET", url, params=querystring)

    json_data = json.loads(response.text)
    print type(json_data)
    return toJson(response.text)


if __name__ == '__main__':
    app.run(debug = True)
