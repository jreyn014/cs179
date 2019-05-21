# file: inquiry.py auth: Albert Huang <albert@csail.mit.edu> desc:
import bluetooth
#import socket
#import sys
print "performing inquiry..."
nearby_devices = bluetooth.discover_devices(lookup_names = True)
print "found %d devices" % len(nearby_devices)
#hostMACAddr = "B8:27:EB:A6:9E7E" #Jesus'
#hostMACAddr = "B8:27:EB:1A:E0:6F" #Nicke's
port = 4
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
j = 0

try:
    for addr, name in nearby_devices:
        print "%s - %s" % (addr, name)
        if str(name) == ("PLUTO"):   #str(name) == ("Novy")
                print ("Found Pi")
		s.connect((addr, port))
		print ("Connected")
                while 1:
		    reply = s.recv(1024)
		    print reply
                    data = str(j)
                    j = j + 1
                    #data = raw_input()
                    if len(data) == 0:
                          break
                    s.send(data)
                    print 'Sent DATA: ' + data
                    #j = j + 1
    print("Devices are not PLUTO")
except:
	print("Error: Closing socket")
	#client.close()
	s.close()
s.close()
