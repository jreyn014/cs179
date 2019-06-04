import bluetooth
import subprocess
import threading
import socket
import globals

def findHostMAC():
    global hostMACAddress
    name = bluetooth.read_local_bdaddr()
    print("Host: %s" % name[0])
    if name[0] == "B8:27:EB:1A:E0:6F":
        print("Nicke")
        hostMACAddress = "B8:27:EB:1A:E0:6F"
    else:
        print("Jesus")
        hostMACAddress = "B8:27:EB:A6:9E:7E"

hostMACAddress = ""#bluetooth.read_local_bdaddr()[0]
#hostMACAddress = "B8:27:EB:1A:E0:6F" #Nicke
#subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
port = 4
backlog = 10
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#s.bind((hostMACAddress, port))
j = ""

def closeSocket():
    global s
    if(globals.client):
        globals.client.shutdown(socket.SHUT_RDRW)
        globals.client.close()
    s.shutdown(socket.SHUT_RDWR)
    s.close()


def send_host(client, data):
    global s
    try:
        j = str(data)
        print("Data: %s" % data)
        if not data:
           print("Data sucks (send) %s" % data)
           return
        #if i == 1:
        client.send(data)
        print("Sent Data: %s" % data)
    except:
        print("No socket created; Did not send")
        s.close()

def send(data):
    global s
    try:
        j = str(data)
        print("Data: %s" % data)
        if not data:
           print("Data sucks (send) %s" % data)
           return
        s.send(data)
        print("Sent Data: %s" % data)
    except:
        print("No socket created; Did not send")
        s.close()



def recv_host(client):
    global s
    try:
        while 1:
            client.send("You are connected")
            print("Waiting for data")
            data = client.recv(size)
            if not data:
                print("Wrong Data %s" % data)
            print("received: %s" % data)
    except:
        print("No socket created")
        s.close()

def recv():
    global s
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

def FindHost():
    global s
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
                #t2 = threading.Thread(target=send)
                t1.start()
                #t2.start()
                #t1.join()
                #t2.join()
                #if t1.is_alive():
                  # print("t1 running")
                return True, t1
                #t1 = threading.Thread(target=recv)
                #t1.start()
                #t1.join()
                #threading.Thread(target=send, daemon=True).start()
        print("Devices are not ", str(name))
        return False, None
    except:
            print("Error: Closing socket")
            #client.close()
            s.close()
            return False, None

def WaitForClient():
    global s
    global hostMACAddress
    #hostMACAddress = "B8:27:EB:A6:9E:7E" #Jesus
    #hostMACAddress = "B8:27:EB:AB:1C:2B" #Josh
    #hostMACAddress = "B8:27:EB:1A:E0:6F" #Nicke
    #hostMACAddress = ""
    print("Hosting")
    subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
    #port = 4
    #backlog = 10
    #size = 1024
    #s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.bind((hostMACAddress, port))
    print("Listening")
    s.listen(backlog)
    #closeSocket()
    try:
        client, clientInfo = s.accept()
        #while 1:
        print("Connected", clientInfo)
            #threading.Thread(target=recv, daemon=True).start()
        t1 = threading.Thread(target=recv_host, args=[client])
        #t2 = threading.Thread(target=send_host, args=[client, 1])
        t1.start()
        #t2.start()
        #t1.join()
        #t2.join()
        return client, t1
                #client.send("You are connected")
                #data = client.recv(size)
                #if not data:
                #        print ("Wrong Data %s" % data)
               # print ("received: %s" % data)
    except:
            print("Closing socket")
            #client.close()
            s.close()

#test = input("h or not: ")
#if test == 'h':
#findHostMAC()
#WaitForClient()
#else:
#findHostMAC()
#FindHost()
#IF CLIENT RUN WaitForClient
#WaitForClient()
#main()
