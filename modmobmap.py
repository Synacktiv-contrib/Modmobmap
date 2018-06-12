#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <sebastien.dudek(<@T>)synacktiv.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return FlUxIuS ;)
# ----------------------------------------------------------------------------

from __future__ import print_function
from utils.logprocess import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mobile network mapping tool with cheap equipments')
    parser.add_argument('-m', '--module', dest='module', required=False, default='servicemode',
            help='Module to use (e.g: "servicemode" by default)')
    parser.add_argument('-n', '--networks', dest='networks', required=False, default=None,
            help='Networks in MCCMNC format splitted with commas')
    parser.add_argument('-o', '--cached_operator', dest='operators', required=False, default=False, action='store_true',
            help='Use operator in cache to speed up the passive scan')
    parser.add_argument('-s', '--sdk', dest='androidsdk', required=False, default='/opt/Android',
            help='Android SDK path')
    parser.add_argument('-a', '--at', dest='atmode', required=False, default=None,
                        help='AT access mode. If host put something like "/dev/ttyUSBxx. By default it uses ADB."')
    parser.add_argument('-f', '--file', dest='file', required=False, default=None,
                                        help='File to parse. For the moment it could be used in combination with AT mode host.')
    args = parser.parse_args()
    sm = ADBshell()
    kb = mKB()
    kb.config['androidsdk'] = args.androidsdk
    sm.androidsdkpath = args.androidsdk
    if args.file is not None:
        kb.config['file'] = args.file
    if args.module == "xgoldmod":
        startXgoldmodCollect()
    else:
        startServiceModeCollect()
    cops = None
    if args.networks is not None:
        printInfo('=> Manual MCC/MNC processing...')
        cops = processManualMCCMN(args.networks) 
    else:
        printInfo('=> Requesting a list of MCC/MNC. Please wait, it may take a while...')
        operators = load_operators()
        if args.operators is True:
            print (bcolors.WARNING+"Found %i operators in cache, you choose to reuse them." % len(operators) + bcolors.ENDC)
            cops = operators
        if cops is None:
            if args.atmode is None:
                cops = sm.getCOPSfromRIL()
            else:
                at = AT(args.atmode)
                cops = at.getCOPS()
            saveMCCMNC(cops)
    if cops is None:
        sys.exit("Problem with AT+COPS=? anwser. Please reboot the phone and try again")
    else:
        print (bcolors.WARNING+"Found %i operator(s)" % len(cops))
        print (cops, bcolors.ENDC)
    operators = [x for x,y in cops.items()]
    if args.atmode is None:
        processOperatorADB(operators)
    else:
        kb.config['tty_file'] = args.atmode
        processOperatorAT(operators)
