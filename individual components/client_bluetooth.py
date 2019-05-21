# file: inquiry.py auth: Albert Huang <albert@csail.mit.edu> desc:
import bluetooth
#import socket
#import sys
print "performing inquiry..."
nearby_devices = bluetooth.discover_devices(lookup_names = True)
print "found %d devices" % len(nearby_devices)

#hostMACAddr = "B8:27:EB:A6:9E7E" #Jesus
#hostMACAddr = "B8:27:EB:1A:E0:6F" #Nicke

port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    for addr, name in nearby_devices:
        print "%s - %s" % (addr, name)
        if str(name) == ("PLUTO"):   #str(name) == ("Novy")
                print ("Found Pi")
		s.connect((addr, port))
		print 'Connected'
                while 1:
                    data = raw_input("Message Something: ")
                    if text == "quit":
                            break
                    s.send(data)
                    print 'Sent DATA: ' + data
                    server, serverInfo = s.accept()
                    response = server.recv(1024)
                    print 'Received: ' + response
    print("Devices are not PLUTO")
except:
	print("No Devices Match: Closing socket")
	#client.close()
	s.close()
