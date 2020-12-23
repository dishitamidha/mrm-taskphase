import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostname()
PORT = 8888
s.bind((HOST, PORT))

print ("Server running...")
textdata = "121311231232132421AIANDAUTOMATION12131243214325124"
while True:
    msg , address = s.recvfrom(1024)
    print("Connected to a client")
    print("Client message: {}".format(msg))
    s.sendto(bytes(textdata).encode("utf-8"), address)
    
    