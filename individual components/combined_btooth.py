import bluetooth
import subprocess
import threading

global s
hostMACAddress = "B8:27:EB:A6:9E:7E" #Jesus
#hostMACAddress = "B8:27:EB:1A:E0:6F" #Nicke
subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
port = 5
backlog = 10
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#s.bind((hostMACAddress, port))
j = 1

def send():
    try:
        data = str(j)
        if not data:
           print("Data sucks (send) %s" % data)
           return
        s.send(data)
        print("Sent Data: %s" % data)
    except:
        print("No socket created; Did not send")
        s.close()



def recv():
    try:
        while 1:
            print("Waiting to receive data")
            data = s.recv(size)
            if not data:
                print("Wrong Data %s" % data)
            print("received: %s" % data)
    except:
        print("No socket created")
        s.close()

def FindClient():
    print ("performing inquiry...")
    nearby_devices = bluetooth.discover_devices(lookup_names = True)
    print ("found %d devices" % len(nearby_devices))

    try:
        for addr, name in nearby_devices:
            print ("%s - %s" % (addr, name))
            if str(name) == ("PLUTO") or str(name) == ("Novy"):
                print ("Found Pi")
                s.connect((addr, port))
                print ("Connected")
                t1 = threading.Thread(target=recv)
                t1.start()
                t1.join()
                #threading.Thread(target=send, daemon=True).start()
        print("Devices are not PLUTO")
    except:
            print("Error: Closing socket")
            #client.close()
            s.close()

def WaitForClient():
    #hostMACAddress = "B8:27:EB:A6:9E:7E" #Jesus
    #hostMACAddress = "B8:27:EB:AB:1C:2B" #Josh
    #hostMACAddress = "B8:27:EB:1A:E0:6F" #Nicke
    #hostMACAddress = ""
    #subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
    #port = 4
    #backlog = 10
    #size = 1024
    #s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    #s.bind((hostMACAddress, port))
    print("Listening")
    s.listen(backlog)
    try:
        client, clientInfo = s.accept()
        #while 1:
        print("Connected", clientInfo)
            #threading.Thread(target=recv, daemon=True).start()
        t2 = threading.Thread(target=send)
        t2.start()
        t2.join()
                #client.send("You are connected")
                #data = client.recv(size)
                #if not data:
                #        print ("Wrong Data %s" % data)
               # print ("received: %s" % data)
    except:
            print("Closing socket")
            #client.close()
            s.close()

#def main():
FindClient()
    #WaitForClient()
#main()
#threading.Thread(target=main).start()
