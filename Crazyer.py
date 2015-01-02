import random
import serial
from HandshakeException import HandshakeException
from Utils import *

EVENT_KEY_PRESS = 1
EVENT_KEY_RELEASE = 2

KEY_CLICK = 0
KEY_SPACE = 1
KEY_UP = 2
KEY_DOWN = 3
KEY_LEFT = 4
KEY_RIGHT = 5

class Crazyer(object):

    def __init__(self, devname, handler):

        self.handler = handler
        self.serial = serial.Serial(devname, baudrate=2400)
        self.serial.setTimeout(1)
        self.handshake()
        self.serial.setTimeout(None)
        self.listen()

    def handshake(self):

        randombyte = inttobytes(random.randint(0, 255))
        handshake_send = (hextobytes('faba') + randombyte)
        self.serial.write(handshake_send)
        self.serial.flush()

        handshake_return = self.serial.read(3)

        if len(handshake_return) != 3 or handshake_return[:len(handshake_return) - 1] != hextobytes('faaa') or handshake_return[2] != handshake_send[2]:
            raise HandshakeException('Didn\'t get the correct handshake return which is %s. Got %s instead.' % (str(hextobytes('faba') + randombyte), str(handshake_return)))

    def listen(self):

        alldata = bytes()

        while 1:

            data = self.serial.read(1)

            if data == bytes.fromhex('fa'):
                alldata = bytes.fromhex('fa')  # reset alldata
                continue

            alldata += data

            # keypress:
            if hextoint('e0') <= data[0] <= hextoint('f5'):
                self.handler.keypress(data[0] - hextoint('e0'))
                continue

            # keyrelease:
            if hextoint('10') <= data[0] <= hextoint('25'):
                self.handler.keyrelease(data[0] - hextoint('10'))
                continue