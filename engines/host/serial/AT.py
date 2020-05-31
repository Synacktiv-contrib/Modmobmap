# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <sebastien.dudek(<@T>)penthertz.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return FlUxIuS ;)
# ----------------------------------------------------------------------------

from __future__ import print_function
import serial

class AT(object):
    tty_int = None
    def __init__(self, tty_path):
        self.tty_int = serial.Serial(tty_path, 115200)

    def _parseCOPS(self, string):
        '''
            Parse AT+COPS=? information
            in(1): string cops returned string
            out: dict infos
        '''
        dict_ = {}
        rstr = string.replace(b'+COPS: ', b'')
        for x in rstr.split(b'),'):
            ysp = x.split(b',')
            if len(ysp) >= 5:
                mccmnc = ysp[3].decode("utf-8").replace('"','')
                netname = ysp[1].decode("utf-8").replace('"','')
                if mccmnc not in dict_:
                    dict_[mccmnc] = netname
        return dict_

    def getCOPS(self):
        tty_int = self.tty_int
        tty_int.write(b'AT+COPS=?\r\n')
        tty_int.readline() # command sent
        result = tty_int.readline()
        #tty_int.readline()
        return self._parseCOPS(result)

    def changePLMN(self, MCCMNC, automode=False):
        mode = 1
        tty_int = self.tty_int
        if automode is True:
            mode = 0
        tty_int.write(b"AT+COPS=%i,2,\"%s\"\r\n" % (mode, MCCMNC.encode('utf-8')))

    def unregister(self):
        tty_int = self.tty_int
        tty_int.write(b"AT+COPS=2\r\n")

    def changeNetworkType(self, type_=2):
        '''
            Change Networktype mode using AT commands
            in(1): int Networktype mode.
                2 for Autoselect, 13 for GSM only and 14 for 3G only.
            out: process result
        '''
        tty_int = self.tty_int
        tty_int.write(b"AT^SYSCONFIG=%i,1,1,2\r\n")

if __name__ == "__main__":
    ser = AT('/dev/ttyACM0')
    print (ser.getCOPS())
    ser.changePLMN(b'20801')
