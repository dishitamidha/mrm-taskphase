import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostname()
PORT = 8888
ServerAddress = (HOST, PORT)
s.sendto(bytes("Hello from client").encode("utf-8"), ServerAddress)

datafromserver = s.recvfrom(1024)
y = datafromserver[0].decode('utf-8')
print ("Text data sent by server: {} ".format(y))