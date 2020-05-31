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
from core.mKB import *
from utils.colors import bcolors

def Cellslogger(func):
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        kb = mKB()
        if 'SM_cells' not in kb.data:
            kb.data['SM_cells'] = {}
        id_ = v = None
        try:
            id_,v = list(result.items())[0]
        except:
            pass
            #print ("Error Celllog: %s" % result)
        if id_ not in kb.data['SM_cells'] and id_ is not None:
            kb.data['SM_cells'][id_] = v
            if kb.config['verbose'] == True:
                string2print = "[+] New cell detected [CellID/PCI-DL_freq  (%s)]" % id_
                string2print += "\n\r Network type=%s" % v['type']
                string2print += "\n\r PLMN=%s" % v['PLMN']
                if 'band' in v:
                    string2print += "\n\r Band=%i" % v['band']
                if '4G' in v['type']:
                    string2print += "\n\r Downlink EARFCN=%i" % v['eARFCN']
                elif '3G' in v['type']:
                    string2print += "\n\r Downlink UARFCN=%i" % v['RX']
                    string2print += "\n\r Uplink UARFCN=%i" % v['TX']
                elif '2G' in v['type']:
                    string2print += "\n\r ARFCN=%i" % v['arfcn']
                print (bcolors.OKGREEN+string2print+bcolors.ENDC)
        return result
    return wrapped
