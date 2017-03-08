import serial
import numpy as np


class StimInterface(object):
    _baudrate = 921600
    _read_length = 37   #40 - 3 (2 for lf and cr, and one for header)

    def __init__(self):
        #self.serial = serial.Serial('/dev/ttyUSB0', baudrate=self._baudrate) #Linux
        self.serial = serial.Serial(port ='COM3', baudrate=self._baudrate)
        self.datagram_identifier = chr(0x93)  # Rate, acceleration, incliination
        self.last_msg = None
        self.inc = None
        self.acc = None
        self.gyro = None
        self.skipped_msgs = 0

    def read_datagram(self):
        while self.last_msg != self.datagram_identifier:
            self.last_msg = self.serial.read(1)
        self.last_msg = self.last_msg + self.serial.read(self._read_length)

    def decode(self):
        start = 0
        self.gyro = np.fromstring(
            b'\x00' + self.last_msg[start + 0:start + 3][::-1] +
            b'\x00' + self.last_msg[start + 3:start + 6][::-1] +
            b'\x00' + self.last_[start + 6:start + 9][::-1],
            dtype='<i'
        ).astype(np.float32) / (2 ** 14)

        start += 10

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
            dtype='<i'
        ).astype(np.float32) / (2 ** 22)


if __name__ == '__main__':
    i = StimInterface()
    while(True):
        i.read_datagram()
        i.decode()
        print "helo"





