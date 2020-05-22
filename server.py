import socket
import threading
import time
import logging
from protocol import *
from datetime import datetime


# Function that resets the connection
def resetCon(sock1: socket):
    global clientAddress
    try:
        sock1.sendto(serverResetCon().encode(), clientAddress)

    except OSError:
        print('OSError57')
    finally:
        sock1.close()





def handshake(sock1: socket):
    untilRequestFromClient(sock1)
    return untilAccept(sock1)


def untilRequestFromClient(sock1: socket):
    firstPartOfHandshake: bool = False
    while firstPartOfHandshake is False:
        # keep receiving incoming message until three way handshake
        data, address = sock1.recvfrom(4096)
        # if the first msg received equals the first msg in the protocol then send accept
        if data.decode() == request(address[0]):
            sock1.sendto(serverAccept(address[0]).encode(), address)
            firstPartOfHandshake = True


def untilAccept(sock1: socket):
    secondPartOfHandshake: bool = False
    while secondPartOfHandshake is False:
        data, address = sock1.recvfrom(4096)
        # if the 2 msg equals the 2 msg in the protocol accept client
        if data.decode() == clientAccept():
            secondPartOfHandshake = True
            timeOfEvent = datetime.now()
            logging.info(str(timeOfEvent) + ': Handshake completed with client with IP address' + str(address))
    return address, secondPartOfHandshake


def testCountMsg(word):
    start = word.find('-')
    end = word.find('=')
    try:
        count = int(word[start + 1:end])
        # if there is no int at between '-' and '=' then raise an error
    except TypeError:
        raise TypeError
    except ValueError:
        raise ValueError
    return count


def receiveMessages(sock1: socket):
    global clientAccepted, count, clientCount


    while clientAccepted is True:
        isMsg: bool
        # sets a timer that runs the reset function when 4.0 sec has elapsed
        t = threading.Timer(4.0, resetCon, args=(sock1,))
        t.start()
        try:
            data, address = sock1.recvfrom(1024)
        except ConnectionResetError:
            print("teehheheheh7")
            break
        except OSError:
            print("teehheheheh5")
            break
        # timer resets after every msg received

        t.cancel()
        try:

            clientCount = testCountMsg(data.decode())

            isMsg = True

        except ValueError:
            isMsg = False
            if data.decode() == heartbeat():

                t.cancel()
            else:
                resetCon(sock1)



        if isMsg:

            if clientCount != count:
                print('Count was: ' + str(count) + ' ClientCount was: ' + str(clientCount))
                clientAccepted = False
                resetCon(sock1)
                break
            print('\nClient: {} '.format(data.decode()))
            count = count + 1
            sock1.sendto(serverMessage(count).encode(), address)
            print('\nServer: {} '.format(serverMessage(count)))
            count = count + 1
    print("hey")



logging.basicConfig(filename='log.txt', level='INFO')
# message count on serverside
count = 0
clientAccepted = False
clientCount = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 20000)
sock.bind(server_address)

clientAddress, clientAccepted = handshake(sock)
receiveMessages(sock)
print("hey")
print("hey")
resetCon(sock)
