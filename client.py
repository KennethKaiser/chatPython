import multiprocessing
import socket
import sys
from configparser import ConfigParser
from pip._vendor.distlib.compat import raw_input
from protocol import *
import threading
import time
import random


def sendHeartbeats():
    global sent, data, server_address, accepted
    while accepted:
        try:
            sent = sock.sendto(heartbeat().encode(), server_address)
            time.sleep(3.0)
            # print('heartbeat')
        except OSError:
            print('Caught OSError')


def chatFunction():
    global sent, data, server_address, accepted, count, server
    if maxPackages > 0:
        testSpamFunction(maxPackages)

    else:

        while accepted:
            st = raw_input("")
            print('\nClient: {}'.format(clientMessage(count, st)))
            sent = sock.sendto(clientMessage(count, st).encode(), server_address)
            count = count + 1
            data, server = sock.recvfrom(4096)

            print('\nServer: {}'.format(data.decode()))

            # sends serverresestcon acknowledgement back
            if data.decode() == serverResetCon():
                print('\nClient: {}'.format(ackReset()))
                sent = sock.sendto(ackReset().encode(), server_address)
                accepted = False
                sock.close()
            count = count + 1


    sock.close()
    sys.exit()


#Didn't work
#def DDoSServer(maxPackages):
#    global count, server_address

 #   """For loop that iterates over the number of package_per_seconds"""
  #  for i in range(maxPackages):
   #     ddos_to_server = "msg-" + str(count) + " = " + "message"
    #    print("C: " + ddos_to_server)

     #   p = multiprocessing.Process(target=sock.sendto, args=(ddos_to_server.encode(), server_address))
      #  p.start()
       # print('hello')




def testSpamFunction(maxPackages):
    global data, server, count, server_address, accepted
    bytes = random._urandom(1024)
    duration = maxPackages;
    timeout = time.time() + duration
    packSent = 0
    try:
        while accepted:
            if time.time() > timeout:
                break
            else:
                pass
            st = "sent %s packets"%(packSent)
            print('\nClient: {}'.format(clientMessage(packSent, bytes)))

            sock.sendto(clientMessage(packSent, bytes).encode(), server_address)
            #sock.sendto(clientMessage(packSent, st).encode(), server_address)
            packSent = packSent + 2
            count = count + 1
            data, server = sock.recvfrom(4096)
            print('\nServer: {}'.format(data.decode()))
            if data.decode() == serverResetCon():
                print('\nClient: {}'.format(ackReset()))
                sock.sendto(ackReset().encode(), server_address)

                accepted = False


    except OSError:
        print('OSError, closing connection')
        sock.close()


config = ConfigParser()
# Read values from config file
config.read('opt.conf.py')
# converting between String and boolean
if config.get('settings', 'keepAlive') == 'True':
    keepAlive = True
elif config.get('settings', 'keepAlive') == 'False':
    keepAlive = False

maxPackages = int(config.get('settings', 'maxPackages'))

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# count message number
count = 0
server_address = ('127.0.0.1', 20000)
# message in three way handshake
message = request(server_address[0]).encode()

accepted = False
# Send data


print('\nClient {}'.format(message.decode()))
sent = sock.sendto(message, server_address)


data, server = sock.recvfrom(4096)
print('\nServer: {}'.format(data.decode()))
if data.decode() == serverAccept(server_address[0]):
    print('\nClient {}'.format(clientAccept()))
    sent = sock.sendto(clientAccept().encode(), server_address)
    accepted = True
else:
    sock.close()

if keepAlive is True & accepted is True:
    t = threading.Timer(3.0, sendHeartbeats)
    t.start()


chatFunction()
