#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <sebastien.dudek(<@T>)penthertz.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return FlUxIuS ;)
# ----------------------------------------------------------------------------

from __future__ import print_function
from core.mLog import Cellslogger
from core.mKB import *

class xgoldmod(object):
    @Cellslogger
    def go2logs(self, cell):
        return cell

    def parseFifo(self):
        kb = mKB()
        FIFO = kb.config['file']
        if 'SM_cells' not in kb.data:
            kb.data['SM_cells'] = {}
        while True:
            with open(FIFO) as fifo:
                while True:
                    data = fifo.read()
                    if len(data) == 0:
                        break
                    infos = data.split(':')[1]
                    isplit = infos.split(';')
                    tmpcell = {}
                    tmpcell2 = {}
                    for cell in isplit:
                        pcell = cell.split('=')
                        tmpcell[pcell[0]] = pcell[1]
                    cid = tmpcell['CID'] + '-' + tmpcell['DL_UARFCN']
                    tmpcell2[cid] = {    'PLMN' : tmpcell['PLMN'],
                                         'RAC' : tmpcell['RAC'],
                                         'LAC' : tmpcell['LAC'],
                                         'type' : '3G',
                                         'RX' : int(tmpcell['DL_UARFCN']),
                                         'TX' : int(tmpcell['UL_UARFCN'].split('\0')[0]),
                                     }
                    self.go2logs(tmpcell2)


