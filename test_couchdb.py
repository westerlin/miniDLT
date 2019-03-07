# -*- coding: utf-8 -*-
import time
prev1 = time.time()

import couchdb,json

with open("../../scripts/couchInfo.json") as json_data:
    d = json.load(json_data)
    json_data.close()

#print(d)

prev2 = time.time()
print(d["url"])
couch = couchdb.Server(d["url"])

#couch.create("mydb")

print("trying to connect to %s" %d["db"])
db = couch[d["db"]]

#newdoc = {"country":"India"}
#db.save(newdoc)
#newdoc = {"block":"testing","name":"law"}
#db.save(newdoc)

otherdoc = {
	"sender":{
		"userid":"raw",
		"organisation":"org1"
		},
	"recipient":{
		"userid":"pmr",
		"organisation":"org2"
		},
	"payload":{
		"hash":"518c565db6a4b5d5a4413d8472b4a1db5068a790245889768271d96675fe4fb9",
		"nonce":100,
		"transaction":{
			"seller":"db",
			"buyer":"pl",
			"isin":"I9982234",
			"price":100,
			"volume":1000,
		}
	}	

}

#db.save(otherdoc)

#mango = {'selector': {'block': 'testing'},'fields': ['name'],'sort':[{'name': 'asc'}]}
#mango = {'selector': {'block': 'testing'},'fields': ['name']}

mango = {'selector': {"payload":{"transaction":{'buyer': 'pl'}}}, "fields":["payload.transaction.isin"]}

mango = {'selector': {'sender': {'userid':"raw"}},'fields': ['payload.transaction.isin']}
#mango = {'selector': {'block': 'testing'}}
prev = time.time()
output = []
for a in range(1):
    for row in db.find(mango):
        output.append(row)  
        
ending = time.time()
print(output)
print("Total find-time:",ending-prev)    
print("Total connect-time:",prev-prev2)    
print("Total runtime:",ending-prev1)    