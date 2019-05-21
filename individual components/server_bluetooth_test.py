import bluetooth
#import socket
#hostMACAddress = "B8:27:EB:A6:9E7E" #Jesus
#hostMACAddress = "B8:27:EB:AB:1C:2B" #Josh
#hostMACAddress = "B8:27:EB:1A:E0:6F" #Nicke
port = 3
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
print("Listening")
s.listen(backlog)
try:
    client, clientInfo = s.accept()
    while 1:
        print("%s connected", clientInfo)
        data = client.recv(size)
        if not data:
            print 'Wrong Data ' + data

	print 'received: ' + data

        echo = "Echo: " + data
        s.send(str(echo))
except:
    print("Closing socket")
    #client.close()
    s.close()
