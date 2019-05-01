import bluetooth
#import socket

hostMACAddress = "B8:27:EB:A6:9E7E"
port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
print("LIstening")
s.listen(backlog)

try:
    print("client")
    client, clientInfo = s.accept()
    while 1:
        print("%s connected", clientInfo)
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)
except:
    print("Closing socket")
    client.close()
    s.close()
