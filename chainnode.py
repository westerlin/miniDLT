import threading, socket, time, json, importlib, yaml, sys
from cryptosign import CryptographicSignature,verifyMessage

class Transaction:
    
    def __init__(self):
        pass


def verifySignature(message,publickey):
    if message.get("payload") and message.get("signature"):
        return verifyMessage(json.dumps(message["payload"]),message["signature"],publickey)

class ChainNode:

    """
    suggest af transaction or af block (including index etc.)

    refused on validity of transaction
    refused due to index or hash
    refused due to previous hash mismatch (maybe because another was linked in)
    """

    def __init__(self,node,nodes,publickey):
        self.portCLI = node.portCLI
        self.portDLT = node.portDLT
        self.host = socket.gethostname()
        self.nodes = nodes
        self.name = node.name
        self.signer = CryptographicSignature()
        self.signer.generate()
        self.publickey = publickey
        self.DLTsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.DLTsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.CLIsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.CLIsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__log__(" Starting services .. on [{}] ".format(self.host))
        self.active = True
        self.service1 = threading.Thread(target=self.__DLTlistener__)
        self.service1.deamon = True
        self.service2 = threading.Thread(target=self.__CLIlistener__)
        self.startServices()
        

    def __log__(self,message):
        print("{}:{}:{}".format(self.name,time.ctime(time.time()),message))

    def startServices(self):
        self.service1.start()
        self.service2.start()
        
        aliveMessage = {"command":"alive","node":{"name":self.name,"host":self.host,"public":self.signer.getPublicKey()}}
        self.__DLTbroadcast__(aliveMessage)
        #self.__log__("Services started")

    def reportNodes(self):
        self.__log__("Reporting on all nodes.")
        output = {}
        i=0
        for node in self.nodes:
            if node.name != self.name:
                if node.public:
                    output["dltNode%d"%i] = {"name":node.name,"clientListenerPort":node.portCLI,"DLTListenerPort":node.portDLT,"host":node.host,"publicKey":node.public}
                    print("\n\tID:%s\n\tPublicKey:%s" %(node.name,node.public))
                else:    
                    output[node.name] = "Not confirmed"
                    print("\n\tID:%s\n\tPublicKey:No confirmed" %(node.name))
                i=i+1    
        return output
                
    def __DLTlistener__(self):
        self.__log__("DLT service started")
        self.DLTsocket.bind((self.host,self.portDLT))
        self.DLTsocket.listen(0)
        self.DLTsocket.setblocking(0)
        self.DLTsocket.settimeout(10)
        while self.active:
            try:
                clientsocket,addr = self.DLTsocket.accept()
                self.__log__("(+) DLT TX from %s" % str(addr))
                maxBytesToReceive = 1024
                tm = clientsocket.recv(maxBytesToReceive)
                self.__log__("  (-) DLT TX recieved:{}".format(tm.decode("utf-8")))
                cmdmsg = json.loads(tm.decode("utf-8"))
                if cmdmsg.get("command") == "alive":
                    node = cmdmsg.get("node")
                    nodeConfig = self.__getNodeByName__(node.get("name"))
                    if nodeConfig:
                        if not nodeConfig.public or nodeConfig.public !=node.get("public"):
                            aliveMessage = {"command":"alive","node":{"name":self.name,"host":self.host,"public":self.signer.getPublicKey()}}
                            self.__DLTgossip__(aliveMessage,nodeConfig)
                        nodeConfig.setPublicKey(node.get("public"))
                        self.__log__("Received alive message from %s" %node.get("name"))
                #currentTime = time.ctime(time.time())+"\r\n"
                #time.sleep(timefreq)
                #clientsocket.send(currentTime.encode("utf-8"))
                #clientsocket.close()
            except socket.error:
                pass

    def __getNodeByName__(self,name):
        for node in self.nodes:
            if name == node.name: return node
        return None

    def __DLTbroadcast__(self,message):
        for node in self.nodes:
            self.__DLTgossip__(message,node)

    def __DLTgossip__(self,message,node):
        if node.portDLT != self.portDLT and node.portCLI != self.portCLI:
            try:
                socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socketclient.connect((node.host,node.portDLT))
                messageString = json.dumps(message).encode("utf-8")
                socketclient.send(messageString)
                socketclient.close()
                self.__log__("    (+) TX send to {}:{}".format(node.host,node.portDLT))
            except socket.error as e:
                self.__log__("    (+) No connection to {}:{} - Error:{} ".format(self.host,self.portDLT,e.strerror))
                pass

    def __CLIlistener__(self):
        self.CLIsocket.bind((self.host,self.portCLI))
        self.CLIsocket.listen(0)
        self.__log__("CLI service started")
        while self.active:
            clientsocket,addr = self.CLIsocket.accept()
            self.__log__("(+) CLI message from %s" % str(addr))
            maxBytesToReceive = 1024
            tm = clientsocket.recv(maxBytesToReceive)
            cmd = json.loads(tm.decode("utf-8"))
            if verifySignature(cmd,self.publickey):
                cmd = cmd["payload"]
                if cmd.get("command") == "stop":
                    self.active = False
                    self.DLTsocket.close()
                    self.CLIsocket.close()
                    self.__log__("Server closes down ... ")
                    clientsocket.send(json.dumps({"response":"OK","message":"Server closes down"}).encode('utf-8'))
                elif cmd.get("command") == "smart":
                    self.invokeSmartContract()
                    clientsocket.send(json.dumps({"response":"OK","message":"Smart contract was invoked"}).encode('utf-8'))
                elif cmd.get("command") == "report":
                    report = {}
                    report["report"] = self.reportNodes()
                    clientsocket.send(json.dumps({"response":"OK","message":report}).encode('utf-8'))
                else:
                    self.__log__("  (+) DLT message :{}".format(tm.decode("utf-8")))
                    self.__DLTbroadcast__(cmd)
                    clientsocket.send(json.dumps({"response":"OK","message":"Echoing message onto miniDLT network"}).encode('utf-8'))
                    #currentTime = time.ctime(time.time())+"\r\n"
            else:
                self.__log__("  (-) DLT message :{}".format(tm.decode("utf-8")))
                clientsocket.send(json.dumps({"response":"Error","message":"TX was not correctly signed."}).encode('utf-8'))


    def invokeSmartContract(self):
        module = importlib.import_module("smartcontract")
        SmartContract = getattr(module,"SmartContract")
        contract = SmartContract()
        self.__log__(contract.execute())

class NodeConfig:

    def __init__(self,name,portCLI,portDLT,DB):
        self.name = name
        self.portCLI = portCLI
        self.portDLT = portDLT
        self.DB = DB
        self.host = socket.gethostname()
        self.public = None
    
    def setPublicKey(self,key):
        self.public = key
        print("Public key included",self.public)

config_file_name = sys.argv[1]
nodeNumber = int(sys.argv[2])
#portDLT = int(sys.argv[3])

with open(config_file_name) as data_file:
    global config
    config = yaml.load(data_file)

nodes = []

try:
    Nodes = config["ChainNodeNet"]["Nodes"]
    users = config["ChainNodeNet"]["Users"]
    publickey=users["User00"]["PublicKey"]
    for key in Nodes.keys():
        #oda = config["ChainNodeNet"][key]["hjh"]
        node = Nodes[key]
        name = Nodes[key]["Name"]
        portCLI = int(Nodes[key]["Ports"]["CLI"])
        portDLT = int(Nodes[key]["Ports"]["DLT"])
        db = Nodes[key]["DB"]
        nodeConfig = NodeConfig(name,portCLI,portDLT,db)
        nodes.append(nodeConfig)
except KeyError as error:
    print("ERROR: Node config for {} was not properly formed".format(key))
    print("Name: <name>")
    print("     Ports:")
    print("         CLI: #000")
    print("         DLT: #000")
    print("     DB: <dbname>")
    print(error)
finally:
    print("Configurations was loaded. Network consists of {} nodes.".format(len(nodes)))
    if nodeNumber < len(nodes):
        print("ChainNode {} will start".format(nodes[nodeNumber].name))
        ChainNode(nodes[nodeNumber],nodes,publickey)
    else:
        print("Requested node {} which was not defined.".format(nodeNumber))


#Network.__dict__ = data["ChainNodeNet"]
#print(Network.ChainNode01["Name"])


#myNode = ChainNode(name,portCLI,portDLT,[(socket.gethostname(),3402),(socket.gethostname(),3412),(socket.gethostname(),3422)])
