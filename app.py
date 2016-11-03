from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
import json, sys
import requests

app = Flask(__name__)
bootstrap = Bootstrap(app)
key = 'AIzaSyCieQLOf0-4RILST4Eivz7CjdOp-4cCUOE'

# print json_data['queries']['request'][0]['count']

def toJson(data):
    line = json.dumps(data)
    return line

@app.route('/')
def index():
    return render_template('index.html',name='yrq')

@app.route('/query/',methods=['GET'])
def query():
    if request.method == 'GET':

        error = 0
        # read engineID
        f = file('data/engine.json')
        s = json.load(f)
        no = 0
        sn = 'engine_' + str(no+1)
        cx = s['engine'][no][sn]['cx']
        engine_name = s['engine'][no][sn]['name']

        # combine search string
        q = request.args.get('q')

        url = "https://www.googleapis.com/customsearch/v1"
        query_string = {"key":key,"cx":cx,"num":"10","q":q}
        # print "quertstring is" + query_string
        response = requests.request("GET", url, params=query_string)
        json_data = json.loads(response.text)

        try :
            json_data['items']
        except:
            # print json_data['error']
            error = 1
            error_msg = 'error_code:' +str(json_data['error']['code'])
            return render_template('index.html',error=error,error_msg=error_msg,engine_name=engine_name)
        # current_page = json_data['queries']['request'][0]['startIndex']/10
        # next_page = current_page+1
        # engine_name = json_data['context']['title']

        result = []
        results = []
        items = json_data['items']

        for item in items:
            result.append(item['title']).append(item['link']).append(item['displayLink']).append(item['snippet']).append(result)
            result =[]
        # print results
            # print ' title:' + item['title']
        # items = json_data['item']
        # print title, link
        # return toJson(response.text)
        # return toJson(items)
        return render_template('index.html',results=results,error=error,engine_name=engine_name)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug = True)
