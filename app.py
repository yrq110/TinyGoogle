# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from flask.ext.bootstrap import Bootstrap
import json, sys
import requests

app = Flask(__name__)
bootstrap = Bootstrap(app)

def toJson(data):
    line = json.dumps(data)
    return line

@app.route('/')
def index():
    return render_template('index.html',name='index')

@app.route('/query/',methods=['GET'])
def query():
    if request.method == 'GET':
        has_result = 0
        error = 0
        q = request.args.get('q')

        # read engineID
        f = file('data/engine.json')
        s = json.load(f)

        for i in range(len(s['engine'])-2) :
            # no = i
            sn = 'engine_' + str(i+1)
            key = s['engine'][i][sn]['key']
            cx = s['engine'][i][sn]['cx']
            engine_name = s['engine'][i][sn]['name']

            # search request
            url = "https://www.googleapis.com/customsearch/v1"
            query_string = {"key":key,"cx":cx,"num":"10","q":q}
            response = requests.request("GET", url, params=query_string)
            json_data = json.loads(response.text)


            try:
                if json_data['items']:
                    has_result = 1
                    break
            except:
                try :
                    json_data['error']
                    if i == len(s['engine'])-3 :
                        error = 1
                        # print json_data
                        error_msg = 'error_code' +str(json_data['error']['code'])
                        return render_template('index.html',error=error,error_msg=error_msg,engine_name=engine_name)
                    else :
                        continue
                except :
                    break


        # next_page = current_page+1
        # engine_name = json_data['context']['title']

        # print json_data

        if has_result == 1 :
            print "have results"
            result = []
            results = []
            items = json_data['items']
            current_page = json_data['queries']['request'][0]['startIndex']/10
            print items
            for item in items:
                result = [item['title'],item['link'],item['displayLink'],item['snippet']]
                results.append(result)
                result =[]
            print results

            search_info =  'About ' + json_data['searchInformation']['formattedTotalResults'] + ' results (' + json_data['searchInformation']['formattedSearchTime'] + ' seconds)'

            return render_template('index.html',results=results,error=error,engine_name=engine_name,search_info=search_info)
        else :
            search_info =  'About ' + json_data['searchInformation']['formattedTotalResults'] + ' results (' + json_data['searchInformation']['formattedSearchTime'] + ' seconds)'
            return render_template('index.html',error=error,engine_name=engine_name,search_info=search_info)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug = True)
