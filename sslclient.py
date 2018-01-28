import socket, ssl, pprint, sys

host = socket.gethostname()
port = 3401
cert_name = "myapp1"
msg_ssl = "sys.args[2]"
#msg_ssl = sys.args[2]

# require a certificate from the server
def sslSender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssl_sock = ssl.wrap_socket(s,
                                certfile="certs/"+cert_name+".crt",
                                keyfile="certs/"+cert_name+".key",
                                #certfile="ssl_cert/"+cert_name+".pem",
                                #keyfile="ssl_cert/"+cert_name+".key",
#                                ca_certs="ssl_cert/"+cert_name+".key",
                                cert_reqs=ssl.CERT_REQUIRED,
                               ssl_version=ssl.PROTOCOL_TLSv1)
    ssl_sock.connect((host, port))
    print("Representation",repr(ssl_sock.getpeername()))
    print("Certificate:",ssl_sock.getpeercert(binary_form=False))
    #print(repr(ssl_sock.get_server_certificate()))
    #print(ssl_sock.get_server_certificate())
    print("Certificate2:",pprint.pformat(ssl_sock.getpeercert()))
    print("Cipher:",ssl_sock.cipher())
    # Set a simple HTTP request -- use http.client in actual code.
    #ssl_sock.write("""GET / HTTP/1.0\rHost: www.verisign.com\r\n\r\n""".encode('utf-8'))
    #ssl_sock.write("EN MEGET HEMMLIG BESKED. MÅ IKKE VISES.".encode('utf-8'))
    ssl_sock.send("EN MEGET HEMMLIG BESKED. MÅ IKKE VISES.".encode('utf-8'))
    # Read a chunk of data.  Will not necessarily
    # read all the data returned by the server.
    #data = ssl_sock.read()
    # note that closing the SSLSocket will also close the underlying socket
    ssl_sock.close()

def normalSender():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    # Set a simple HTTP request -- use http.client in actual code.
    #ssl_sock.write("""GET / HTTP/1.0\rHost: www.verisign.com\r\n\r\n""".encode('utf-8'))
    s.send("EN MEGET HEMMLIG BESKED. MÅ IKKE VISES.".encode('utf-8'))
    # Read a chunk of data.  Will not necessarily
    # read all the data returned by the server.
    #data = s.read()
    # note that closing the SSLSocket will also close the underlying socket
    s.close()

#print(ssl.get_server_certificate((host,port),ssl_version=ssl.PROTOCOL_TLSv1))
sslSender()
#normalSender()
