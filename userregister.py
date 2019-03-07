"""

    Testing of editor
    Building ClientUser Class

"""

import json
#from cryptosign import CryptographicSignature
	
class ClientUser:
    
    def __init__(self,userdata=None):
        if userdata:
            self.name=userdata["name"]
            self.publickey = userdata["pubkey"]
            self.org=userdata["org"]
            self.gateways=userdata["gateways"]
            self.roles=userdata["roles"]

class ClientRegister:
    
    def __init__(self):
        self.register = {}

    def addUser(self, user):
        self.register[user.name]=user
        
    def getUser(self, name):
        return self.register.get(name)
        
    def toJSON(self):
        return json.dumps(self.register)
