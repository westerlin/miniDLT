import socket, ssl

#bindsocket = socket.socket()
bindsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
bindsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = socket.gethostname()
port = 3401
print (host)
bindsocket.bind((host, port))
bindsocket.listen(5)

def deal_with_client(connstream):
    data = connstream.read()
    # null data means the client is finished with us
    while data:
      if data:
         print(data.decode('utf-8'))
         # we'll assume do_something returns False
         # when we're finished with client
         break
      data = connstream.read()
    # finished with client
    connstream.close()

cert_name = "myapp1"

while True:
   newsocket, fromaddr = bindsocket.accept()
   connstream = ssl.wrap_socket(newsocket,
                                server_side=True,
                                certfile="certs/"+cert_name+".crt",
                                keyfile="certs/"+cert_name+".key",
                                #certfile="ssl_cert/"+cert_name+".pem",
                                #keyfile="ssl_cert/"+cert_name+".key",
#                                ca_certs="ssl_cert/"+cert_name+".key",
                                 cert_reqs=ssl.CERT_REQUIRED,
#                                certfile="/ssl_cert/cert.pem",
#                                keyfile="/ssl_cert/key.pem",
                                ssl_version=ssl.PROTOCOL_TLSv1)
   deal_with_client(connstream)
