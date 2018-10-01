# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 12:28:39 2018

@author: Mustafa

Web server built using flask library configured to run on local host at port 80
/shorten_url route endpoint accepts a {"url": url} json POST request to generate a shortener code
/<url_code> is a variable url route which returns original url shortened through the api endpoint POST request in response to a GET request
"""

from flask import Flask, jsonify, request
import requests
import json


#import shortener class
from shortener import UrlShortener


#populate a dictionary with pre-existing urls and their class_ids(id in the shortener instance) from the db(json file here)
cons = {}
with open('datastore.json', 'r') as datastore:
    #each line in the json file containse a {"url":url, "class_id":class_id} datapoint
    lines = datastore.readlines()
    #if the file has data (not empty), populate the constructor dictionary with each url as a key and class_id as a value
    if len(lines) > 0:
        for i in lines:
            dic = json.loads(i)
            cons[dic["url"].encode('utf-8')] = int(dic['class_id'])

datastore.close()
            

#shortener instance
shortener_ins = UrlShortener(cons)

print 'loading existing urls...'

#a dictionary containing each shortened url and corresponding shotener code
url2code = {}
for i in shortener_ins.url2id.keys():
    url2code[i] = shortener_ins.shorten_url(i)


#for checking if a url is valid during processing the post request
def validate_url(url):
    print 'validating url....'
    if url[0:4] == 'http':
        res = requests.get(url)
    else:
        res = requests.get('http://'+url)
    
    if res.status_code == 404:
        return 'invalid'
    
#initialise the app
app = Flask(__name__)

#for returning the shortened url from the post request

service = 'http://localhost/'

#route has a variable url name url_code, read from url2code dictionary
@app.route('/<url_code>')
def redirector(url_code):
    for i, j in url2code.items():
        if url_code == j:
            return i

            
#the url shortening endpoint
@app.route('/shorten_url', methods = ['GET','POST'])
def main():
    #in case a GET request is made to the API endpoint
    if request.method == 'GET':
        s = request.get_json()
        if s == None:
            return 'This Endpoint accepts only POST requests'

            
    
    if request.method == 'POST':
        #read request json and convert to dictionary
        s = request.get_json()
        #there should only be one value in the json body
        req_url = s.values()[0]
        #check url validity
        if validate_url(req_url) == 'invalid':
            return 'The url you have entered is invalid'
        else:
            #run through the shortener instance to get shortener code
            #if the identical url exists withing the db/instance already, it will return the same code
            code = shortener_ins.shorten_url(req_url)
            #append to url2code for when a get request was made to the shortened url in the same session
            url2code[req_url] = code
            #get class_id from the instance in order to append to the db
            req_url_class_id = shortener_ins.url2id[req_url]
            #create dictionary entry to append to the json file
            entry = {'url':req_url, 'class_id':req_url_class_id}
            print 'inserting url {} with class_id {} into the datastore'.format(entry['url'],entry['class_id'])
            #append entry to the json file
            with open('datastore.json', 'a') as datastore:
                datastore.write('{}\n'.format(json.dumps(entry)))
            datastore.close()
            return jsonify({'shortened_url': service+code}), 201
            

        
#running on localhost at port 80 
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=80, debug = True)
