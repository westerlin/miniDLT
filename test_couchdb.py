# -*- coding: utf-8 -*-
import time
prev1 = time.time()

import couchdb,json

with open("../../scripts/couchInfo.json") as json_data:
    d = json.load(json_data)
    json_data.close()

#print(d)

prev2 = time.time()
couch = couchdb.Server(d["url"])
db = couch[d["db"]]

#newdoc = {"country":"India"}
#db.save(newdoc)
#newdoc = {"block":"testing","name":"law"}
#db.save(newdoc)

#mango = {'selector': {'block': 'testing'},'fields': ['name'],'sort':[{'name': 'asc'}]}
mango = {'selector': {'block': 'testing'},'fields': ['name']}
#mango = {'selector': {'block': 'testing'}}
prev = time.time()
output = []
for a in range(1):
    for row in db.find(mango):
        output.append(row["name"])  
        
ending = time.time()
#print(output)
print("Total find-time:",ending-prev)    
print("Total connect-time:",prev-prev2)    
print("Total runtime:",ending-prev1)    