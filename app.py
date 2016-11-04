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
        start_index = request.args.get('start')
        # read engineID
        f = file('data/engine.json')
        s = json.load(f)

        for i in range(len(s['engine'])-2) :
            sn = 'engine_' + str(i+1)
            key = s['engine'][i][sn]['key']
            cx = s['engine'][i][sn]['cx']
            engine_name = s['engine'][i][sn]['name']

            # search request
            url = "https://www.googleapis.com/customsearch/v1"
            if start_index :
                query_string = {"key":key,"cx":cx,"num":"10","q":q,"start":start_index}
            else :
                query_string = {"key":key,"cx":cx,"num":"10","q":q}
            response = requests.request("GET", url, params=query_string)
            json_data = json.loads(response.text)

            try:
                # case 1: has results
                if json_data['items']:
                    has_result = 1
                    break
            except:
                # case 2: error
                try :
                    json_data['error']
                    if i == len(s['engine'])-3 :
                        error = 1
                        # print json_data
                        error_msg = 'error_code' +str(json_data['error']['code'])
                        return render_template('index.html',q=q,error=error,error_msg=error_msg,engine_name=engine_name)
                    else :
                        continue
                # case 3: no results
                except :
                    break

        if has_result == 1 :
            # print "have results"
            result = []
            results = []
            items = json_data['items']
            current_start_index = json_data['queries']['request'][0]['startIndex']
            if current_start_index == 1 :
                has_previous = 0
                search_info =  'About ' + json_data['searchInformation']['formattedTotalResults'] + ' results (' + json_data['searchInformation']['formattedSearchTime'] + ' seconds)'
            else :
                has_previous = 1
                search_info =  "Page " + str(current_start_index/10+1) + ' of About ' + json_data['searchInformation']['formattedTotalResults'] + ' results (' + json_data['searchInformation']['formattedSearchTime'] + ' seconds)'
            print items
            for item in items:
                result = [item['title'],item['link'],item['displayLink'],item['snippet']]
                results.append(result)
                result =[]
            # print results



            return render_template('index.html',q=q,results=results,error=error,engine_name=engine_name,search_info=search_info,has_previous=has_previous,current_start_index=current_start_index)
        else :
            search_info =  'About ' + json_data['searchInformation']['formattedTotalResults'] + ' results (' + json_data['searchInformation']['formattedSearchTime'] + ' seconds)'
            return render_template('index.html',q=q,error=error,engine_name=engine_name,search_info=search_info)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug = True)
