import socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ""
PORT = 8888 
s.connect((HOST, PORT))
textdata = ""
conn = True
while conn:
    chunk= s.recv(10)
    if len(chunk)<=0:
        conn = False
    else:
        textdata += chunk.decode("utf-8") 
print (textdata)
