import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ""
PORT = 8888
s.bind((HOST, PORT))
s.listen(5)
print ("Server listening...")

while True:
    conn, address = s.accept()
    print ("Server connected to {}".format(address))
    print ("Sending text data to client...")
    conn.send(bytes("121311231232132421AIANDAUTOMATION12131243214325124").encode("utf-8"))
    print("Sent")

    conn.close()
    print ("Connection terminated")