# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 08:48:52 2018

@author: raw

set FLASK_APP=<name of py programme>
set FLASK_DEBUG=1
"""

from flask import Flask, request, render_template, jsonify
import socket,json
from cryptosign import CryptographicSignature

#import hashlib

app = Flask(__name__)

host = socket.gethostname()
port = 3401

def sendMessage(port, message):
    try:
        socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketclient.connect((host,port))
        socketclient.send(message.encode("utf-8"))
        data = socketclient.recv(1024)
        socketclient.close()
        return True,data
    except socket.error:
        return False,None

def call_miniDLT(data):
    jsMsgObj = json.loads(data.decode())
    return sendMessage(jsMsgObj["port"],json.dumps(jsMsgObj["payload"]))

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/json', methods=['POST','GET'])
def my_form_post():
    print("Received input")
    print(request.data)
    cryptosigner = CryptographicSignature()
    cryptosigner.generate()
    #ct = CryptographicSignature(cryptosigner.getPrivateKey())
    #tidligere valideringscheck her- men det virker 
    #ct er en reetablering ud fra privatekey streng fra Cryptosigner
    return jsonify({"message":{"base":{"privateKey":cryptosigner.getPrivateKey(),"publicKey":cryptosigner.getPublicKey()} } })

@app.route('/miniDLT', methods=['POST','GET'])
def ping_miniDLT():
    res,data = call_miniDLT(request.data)
    if res:
        #jsMsgObj = json.loads(request.data.decode())
        return data
    else:
        return jsonify({"message":"There was an error while contacting Node."})

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0',debug=True,port=80)
