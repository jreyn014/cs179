import bluetooth
import subprocess
import threading

global s

def recv():
	while 1:
		data = s.recv(size)
		if not data:
			print("Wrong Data %s" % data)
		print("received: %s" % data)


def WaitForClient():
	hostMACAddress = "B8:27:EB:A6:9E:7E" #Jesus
    #hostMACAddress = "B8:27:EB:AB:1C:2B" #Josh
    #hostMACAddress = "B8:27:EB:1A:E0:6F" #Nicke
	#hostMACAddress = ""
	subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
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
	    #threading.Thread(target=recv, daemon=True).start()
		#
			client.send("You are connected")
			data = client.recv(size)
			if not data:
				print ("Wrong Data %s" % data)
			print ("received: %s" % data)
	except:
		print("Closing socket")
            #client.close()
		s.close()

def main():
    WaitForClient()
    s.close()

threading.Thread(target=main).start()
