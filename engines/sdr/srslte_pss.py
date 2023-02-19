#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <sebastien.dudek(<@T>)penthertz.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return FlUxIuS ;)
# 
# We'd like to thank our contributors for maintening this code:
# - @h0rac (Grzegorz Wypych) from PWNSec.pl
# ----------------------------------------------------------------------------

from __future__ import print_function
from core.mLog import Cellslogger
from core.mKB import *
import os

class srslte_pss(object):
    @Cellslogger
    def go2logs(self, cell):
        return cell

    def parseFifo(self):
        kb = mKB()
        FIFO = kb.config['file']
        if os.path.isfile(FIFO) == False:
            try:
                os.mkfifo(FIFO)
            except:
                pass
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
                    cid = tmpcell['CID'] + '-' + tmpcell['DL_EARFCN']
                    tmpcell2[cid] = {    'FREQ' : tmpcell['FREQ'],
                                         'PLMN' : "-1",
                                         'type' : "4G",
                                         'band' : "-1",
                                         'eARFCN' : int(tmpcell['DL_EARFCN']),
                                         'POWER' : tmpcell['POWER'].split("\n")[0], 
                                     }
                    self.go2logs(tmpcell2)


