import socket,os,json

print("CLI interface")

active = True

host = socket.gethostname()
port = 3401

def sendMessage(port, message):
    try:
        socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketclient.connect((host,port))
        socketclient.send(message.encode("utf-8"))
        socketclient.close()
    except socket.error:
        pass

while active:
    cmd = input(">>Commmand:")
    words = cmd.split(",")
    if len(words)>1:
        port = int(words[0])
        msg = words[1]
    else:
        msg = words[0]


    if msg == "exit":
        active = False
    elif msg == "new":
        os.system("start cmd /t:2A /K \"nodestart 0\"") 
        os.system("start cmd /t:3B /K \"nodestart 1\"") 
        os.system("start cmd /t:4C /K \"nodestart 2\"") 
    else:    
        #sendMessage(port,msg)
        messageObj = {"command":msg}
        messageString = json.dumps(messageObj)
        sendMessage(port,messageString)
        print(" (+) OK")
