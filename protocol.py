# Hack protocol requst
def requestHack(clientIP):
    return 'lol-02 {}.'.format(clientIP)

def request(clientIP):
    return 'com-0 {}.'.format(clientIP)


def serverAccept(serverIP):
    return 'com-0 accept {}.'.format(serverIP)


def clientAccept():
    return 'com-0 accept'

def clientAcceptHack():
    return 'hack-123 accept'

def clientMessage(number, msg):
    return 'msg-{}={}'.format(number, msg)


def serverMessage(number):
    return 'res-{}=hey'.format(number)


def serverResetCon():
    return 'con-res 0xFE'


def ackReset():
    return 'con-res 0xFF'


def heartbeat():
    return 'con-h 0x00'