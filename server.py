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
        print(validate_ip('127.0.0.1'))
        data, address = sock1.recvfrom(4096)

        # if the first msg received equals the first msg in the protocol then send accept
        print()
        if data.decode() == request(address[0]) and validate_ip(address[0]) == True:
            print("my timemachineworks")
            sock1.sendto(serverAccept(address[0]).encode(), address)
            firstPartOfHandshake = True
        else:
            timeOfEvent = datetime.now()
            logging.info(str(timeOfEvent) + ": Handshake didn't complete. Either not an IP address or wrong request "
                                            "protocol message ")


def untilAccept(sock1: socket):
    secondPartOfHandshake: bool = False
    while secondPartOfHandshake is False:

        data, address = sock1.recvfrom(4096)
        timeOfEvent = datetime.now()
        # if the 2 msg equals the 2 msg in the protocol accept client
        if data.decode() == clientAccept():
            secondPartOfHandshake = True
            handshakeComplete = True
            logging.info(str(timeOfEvent) + ': Handshake completed with client with IP address' + str(address))


        else:
            secondPartOfHandshake = True
            handshakeComplete = False
            logging.info(str(timeOfEvent) + ": Handshake didn't complete. Wrong protocol accept message")

    return address, handshakeComplete


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
    print("kig her pls" + str(count))
    return count


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def receiveMessages(sock1: socket):
    global clientAccepted, count, clientCount

    serverMessageCount = 1
    while clientAccepted is True:
        isMsg: bool
        # sets a timer that runs the reset function when 4.0 sec has elapsed
        t = threading.Timer(4.0, resetCon, args=(sock1,))
        t.start()
        try:
            data, address = sock1.recvfrom(1024)
        except ConnectionResetError:
            break
        except OSError:
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


            if serverMessageCount == clientCount + 1:



                print('\nClient: {} '.format(data.decode()))

                sock1.sendto(serverMessage(serverMessageCount).encode(), address)
                print('\nServer: {} '.format(serverMessage(serverMessageCount)))
                serverMessageCount = serverMessageCount + 2

            else:
                logging.info(": Wrong count in messages")
                clientAccepted = False


    timeOfEvent = datetime.now()
    logging.info(str(timeOfEvent) + ": Resetting Connection")
    resetCon(sock1)


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
resetCon(sock)

# Check for count Ip address check if It is ip address and last part of assignment (hacking)
