import bluetooth
import socket
hostMACAddress = "B8:27:EB:A6:9E:7E" #Jesus
#hostMACAddress = "B8:27:EB:AB:1C:2B" #Josh
#hostMACAddress = "B8:27:EB:1A:E0:6F" #Nicke
#hostMACAddress = ""
port = 4
backlog = 10
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
print("Listening")
s.listen(backlog)

try:
    client, clientInfo = s.accept()
    while 1:
        print("Connected", clientInfo)
	client.send("Hello")
	data = client.recv(size)
        if not data:
            print ("Wrong Data %s" % data)

	print ("received: %s" % data)
#	print ("Info: %s" % info)

#        echo = info
#        s.send(str(echo))

except:
    print("Closing socket")
    #client.close()
    s.close()
