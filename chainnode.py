
import threading, socket, time, json
import importlib

import yaml

class ChainNode:

    """
    suggest af transaction or af block (including index etc.)

    refused on validity of transaction
    refused due to index or hash
    refused due to previous hash mismatch (maybe because another was linked in)
    """

    def __init__(self,node,nodes):
        self.portCLI = node.portCLI
        self.portDLT = node.portDLT
        self.host = socket.gethostname()
        self.nodes = nodes
        self.name = node.name
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
        #self.__log__("Services started")

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
                #currentTime = time.ctime(time.time())+"\r\n"
                #time.sleep(timefreq)
                #clientsocket.send(currentTime.encode("utf-8"))
                #clientsocket.close()
            except socket.error:
                pass

    def __DLTbroadcast__(self,message):
        for node in self.nodes:
            if node.portDLT != self.portDLT and node.portCLI != self.portCLI:
                try:
                    socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socketclient.connect((node.host,node.portDLT))
                    messageString = json.dumps(message).encode("utf-8")
                    socketclient.send(messageString)
                    socketclient.close()
                    #socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    #socketclient.connect((host,port))
                    #socketclient.send(message.encode("utf-8"))
                    #maxBytesToReceive = 1024
                    #tm = socketclient.recv(maxBytesToReceive)
                    #socketclient.close()
                    self.__log__("    (+) TX send to {}:{}".format(node.host,node.portDLT))
                    #print("The time got from the server is %s" % tm.decode("utf-8"))
                except socket.error as e:
                    #self.__log__("    (+) No connection to {}:{} - Error:{} ".format(host,port,e.strerror))
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
            if cmd.get("command") == "stop":
                self.active = False
                self.DLTsocket.close()
                self.CLIsocket.close()
                self.__log__("Server closes down ... ")
            elif cmd.get("command") == "smart":
                self.invokeSmartContract()
            else:
                self.__log__("  (+) DLT message :{}".format(tm.decode("utf-8")))
                self.__DLTbroadcast__(cmd)
                #currentTime = time.ctime(time.time())+"\r\n"

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

import sys

config_file_name = sys.argv[1]
nodeNumber = int(sys.argv[2])
#portDLT = int(sys.argv[3])

with open(config_file_name) as data_file:
    global config
    config = yaml.load(data_file)

nodes = []

try:
    for key in config["ChainNodeNet"].keys():
        #oda = config["ChainNodeNet"][key]["hjh"]
        node = config["ChainNodeNet"][key]
        name = config["ChainNodeNet"][key]["Name"]
        portCLI = int(config["ChainNodeNet"][key]["Ports"]["CLI"])
        portDLT = int(config["ChainNodeNet"][key]["Ports"]["DLT"])
        db = config["ChainNodeNet"][key]["DB"]
        nodeConfig = NodeConfig(name,portCLI,portDLT,db)
        nodes.append(nodeConfig)
except KeyError:
    print("ERROR: Node config for {} was not properly formed".format(key))
    print("Name: <name>")
    print("     Ports:")
    print("         CLI: #000")
    print("         DLT: #000")
    print("     DB: <dbname>")
finally:
    print("Configurations was loaded. Network consists of {} nodes.".format(len(nodes)))
    if nodeNumber < len(nodes):
        print("ChainNode {} will start".format(nodes[nodeNumber].name))
        ChainNode(nodes[nodeNumber],nodes)
    else:
        print("Requested node {} which was not defined.".format(nodeNumber))


#Network.__dict__ = data["ChainNodeNet"]
#print(Network.ChainNode01["Name"])


#myNode = ChainNode(name,portCLI,portDLT,[(socket.gethostname(),3402),(socket.gethostname(),3412),(socket.gethostname(),3422)])
