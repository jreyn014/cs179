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

hostMACAddress = "" #bluetooth.read_local_bdaddr()[0]
#hostMACAddress = "B8:27:EB:1A:E0:6F" #Nicke
#subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
port = 4
backlog = 10
size = 1024
s = None
#s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#s.bind((hostMACAddress, port))
j = ""

def closeSocket():
    global s
    try:
        globals.client.shutdown(socket.SHUT_RDWR)
        globals.client.close()
        s.shutdown(socket.SHUT_RDWR)
        print("closeSocket() closed")
        s.close()
    except:
        print("Socket already closed")
        return


def send_host(client, data):
    global s
    try:
        j = str(data)
        print("Data: %s" % data)
        if not data:
           print("Data sucks (send) %s" % data)
           closeSocket()
           return
        #if i == 1:
        client.send(j)
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
           #closeSocket()
           return
        s.send(j)
        print("Sent Data: %s" % data)
    except:
        print("No socket created; Did not send")
        s.close()

def processData(data):
    data = data.decode()
    print("Decoded: ", data)
    if data == "GAME_OVER":
       globals.game_play = False
       globals.output_win = True
       print("output win from btooth:",globals.output_win)
       globals.output_game_over_multiplayer = True
       if globals.client:
          closeSocket()
          globals.client = None
       globals.recv_thread.join()
       globals.recv_thread = None
    elif data == "You are connected":
       pass
    elif data.isdigit():
       lines = int(data)
       globals.atk_in += lines

def recv_host(client):
    global s
    try:
        client.send("You are connected")
        while 1:
            print("Waiting for data")
            data = client.recv(size)
            print("received: %s" % data)
            processData(data)
            if not data:
                print("Wrong Data %s" % data)
                break
            #print("received: %s" % data)
    except:
        print("Socket Closed")
        s.close()

def recv():
    global s
    try:
        while 1:
            print("Waiting to receive data")
            data = s.recv(size)
            print("received: %s" % data)
            processData(data)
            if not data:
                print("Wrong Data %s" % data)
                break
           # print("received: %s" % data)
    except:
        print("Socket Closed")
        s.close()

def FindHost():
    global s
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
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
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try:
       s.bind((hostMACAddress, port))
    except:
       print("Bind is in use")
       pass
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
