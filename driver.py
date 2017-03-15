import serial
import numpy as np
import time


class StimInterface(object):
    _baudrate = 921600
    _read_length = 39   #40 - 3 (2 for lf and cr, and one for header)
    null_byte = b'\x00'

    def __init__(self):
        #self.serial = serial.Serial('/dev/ttyUSB0', baudrate=self._baudrate) #Linux
        self.serial = serial.Serial(port ='COM5', baudrate=self._baudrate, timeout=None)
        self.datagram_identifier = b'\x93'  # Rate, acceleration, incliination
        self.last_msg = None
        self.inc = None
        self.acc = None
        self.gyro = None
        self.skipped_msgs = 0

    #Decodes 3x 3-byte-fixed-point sections
    def decode_section(self, divisor, byte_offset):
        return (np.fromstring(self.last_msg[byte_offset+0:byte_offset+3] + b'\x00' +
                     self.last_msg[byte_offset+3:byte_offset+6] + b'\x00' +
                     self.last_msg[byte_offset+6:byte_offset+9] + b'\x00',
                        dtype='>i').astype(np.float32) / (2 ** (divisor+8)))

    def read_datagram(self):
        self.last_msg = None
        while self.last_msg != self.datagram_identifier:
            self.last_msg = self.serial.read(1)
        self.last_msg = self.last_msg + self.serial.read(self._read_length)

    def decode(self):
        self.gyro = self.decode_section(byte_offset=1, divisor=14)
        self.acc = self.decode_section(byte_offset=11, divisor=19)
        self.inc = self.decode_section(byte_offset=21, divisor=22)

        self.serial.flushInput()

if __name__ == '__main__':
    i = StimInterface()
    while(True):
        i.read_datagram()
        i.decode()
        print("@", time.clock(), ", gyro:", i.gyro, ", acc:", i.acc, ", inc:", i.inc)
        time.sleep(1)





