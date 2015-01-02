import struct


def hextobytes(string):
    return bytes.fromhex(string)

def inttobytes(integer):
    assert 0 <= integer <= 255
    return bytes([struct.pack('i', integer)[0]])

def hextoint(string):
    return hextobytes(string)[0]