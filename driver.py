import serial
import numpy as np
import time


class StimInterface(object):
    _baudrate = 921600
    _read_length = 37   #40 - 3 (2 for lf and cr, and one for header)
    _gyro = None
    _acc = None
    _inc = None

    def __init__(self):
        #self.serial = serial.Serial('/dev/ttyUSB0', baudrate=self._baudrate) #Linux
        self.serial = serial.Serial(port ='COM5', baudrate=self._baudrate, timeout=None)
        self.datagram_identifier = b'\x93'  # Rate, acceleration, incliination
        self.last_msg = None
        self.inc = None
        self.acc = None
        self.gyro = None
        self.skipped_msgs = 0

    def read_datagram(self):
        self.last_msg = None
        while self.last_msg != self.datagram_identifier:
            self.last_msg = self.serial.read(1)
            #print(b'\x93')
            print(self.last_msg)
            #time.sleep(1)
        self.last_msg = self.last_msg + self.serial.read(self._read_length)

    def decode(self):
        start = 0
        print('Decoding')
        self.gyro = np.fromstring(
            b'\x00' + self.last_msg[start + 0:start + 3][::-1] +
            b'\x00' + self.last_msg[start + 3:start + 6][::-1] +
            b'\x00' + self.last_msg[start + 6:start + 9][::-1],
            dtype='<i'
        ).astype(np.float32) / (2 ** 14)

        start += 10
        print('Reading ACC')
        # acc
        self.acc = np.fromstring(
            b'\x00' + self.last_msg[start + 0:start + 3][::-1] +
            b'\x00' + self.last_msg[start + 3:start + 6][::-1] +
            b'\x00' + self.last_msg[start + 6:start + 9][::-1],
            dtype='<i'
        ).astype(np.float32) / (2 ** 19)
        start += 10

        # inc
        self.inc = np.fromstring(
            b'\x00' + self.last_msg[start + 0:start + 3][::-1] +
            b'\x00' + self.last_msg[start + 3:start + 6][::-1] +
            b'\x00' + self.last_msg[start + 6:start + 9][::-1],
            dtype='>i'
        ).astype(np.float32) / (2 ** 22)

        _gyro = self.gyro
        _inc = self._inc
        _acc = self.acc


if __name__ == '__main__':
    i = StimInterface()
    while(True):
        print('Reading Data')
        i.read_datagram()
        print('Decoding Data')
        i.decode()
        print(i.gyro)
        print(i.acc)
        print(i.inc)
        time.sleep(4)





