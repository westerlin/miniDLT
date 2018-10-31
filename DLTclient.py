# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 08:48:52 2018

@author: raw

set FLASK_APP=<name of py programme>
set FLASK_DEBUG=1
"""

from flask import Flask, request, render_template, jsonify
#import os,socket,json
#import hashlib

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/json', methods=['POST','GET'])
def my_form_post():
    print("Received input")
    print(request.data)
    return jsonify({"message":"Hello there"})

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0',debug=True,port=80)
