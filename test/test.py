import unittest
import Crazyer
from CrazyerHandler import CrazyerHandler

class SimpleHandler(CrazyerHandler):

    def keypress(self, key):
        print('got keypress:', key)

    def keyrelease(self, key):
        print('got keyrelease:', key)

crayzer = Crazyer.Crazyer('/dev/ttyUSB0', SimpleHandler())