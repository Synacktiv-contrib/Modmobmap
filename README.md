Modmobmap
==========

Modmobmap is a tool aimed to retrieve information of cellular networks.
As shown in the first [presentation made at BeeRump 2018](https://www.rump.beer/2018/slides/modmobmap.pdf), this tool is able to retrieve information of 2G, 3G, 4G and more cellular network types with minimum requierement: only a phone with ServiceMode.

For the moment, the tool has only been tested and developped for the following devices:
- Samsung Galaxy S3 via [xgoldmon (Modmobmap's edition)](https://github.com/FlUxIuS/xgoldmon);
- Samsung Galaxy S4;
- Samsung Galaxy S5;
- Samsung Galaxy Note 2 with LTE;

Moreover, as it's compatible for XGold via Modmobmap's forked of *xgoldmon*, this tools should also be able to work with device supported by *xgoldmon* as well:
- Samsung Galaxy S4 GT-I9500 (this is the version without LTE!)
- Samsung Galaxy Nexus GT-I9250 (has to be rooted!)
- Samsung Galaxy S2 GT-I9100
- Samsung Galaxy Note 2 GT-N7100

Note that all devices should be rooted. In any other case, you will have to use the DFR technique by hand!

Also: Patches, or engines, for other devices are very much welcomed! ;)

Requirements
-------------

Here are the following requirements:
- Python 2 or 3;
- Last Android SDK to run ADB: https://developer.android.com/studio/#downloads;
- A compatible mobile phone;
- A valid/unvalid SIM card (just in case to provide an IMSI number).

How to use
----------

The tool is provided with a quick help that shows you the required argument as follows:

```
python modmobmap.py -h
usage: modmobmap.py [-h] [-m MODULE] [-n NETWORKS] [-o] [-s ANDROIDSDK]
                    [-a ATMODE] [-f FILE]

Mobile network mapping tool with cheap equipments

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE, --module MODULE
                        Module to use (e.g: "servicemode" by default)
  -n NETWORKS, --networks NETWORKS
                        Networks in MCCMNC format splitted with commas
  -o, --cached_operator
                        Use operator in cache to speed up the passive scan
  -s ANDROIDSDK, --sdk ANDROIDSDK
                        Android SDK path
  -a ATMODE, --at ATMODE
                        AT access mode. If host put something like
                        "/dev/ttyUSBxx. By default it uses ADB."
  -f FILE, --file FILE  File to parse. For the moment it could be used in
                        combination with AT mode host.
```

Assuming the Android SDK is installed in */opt/Android*, the tool can be quickly started as follows:

```
$ sudo python modmobmap.py
=> Requesting a list of MCC/MNC. Please wait, it may take a while...
Found 2 operator(s)
{u'20810': u'F SFR', u'20820': u'F-Bouygues Telecom'} 
[+] Unregistered from current PLMN
[+] New cell detected [CellID/PCI-DL_freq  (4XXX-81)]
 Network type=2G
 PLMN=208-10
 ARFCN=81
[+] New cell detected [CellID/PCI-DL_freq  (6XXXXXX-2950)]
 Network type=3G
 PLMN=208-20
 Band=8
 Downlink UARFCN=2950
 Uplink UARFCN=2725
[+] New cell detected [CellID/PCI-DL_freq  (3XX-6300)]
 Network type=4G
 PLMN=208-10
 Band=20
 Downlink EARFCN=6300
[+] New cell detected [CellID/PCI-DL_freq  (3XX-2825)]
 Network type=4G
 PLMN=208-10
 Band=7
 Downlink EARFCN=2825
[+] New cell detected [CellID/PCI-DL_freq  (3XX-1675)]
 Network type=4G
 PLMN=208-10
 Band=3
 Downlink EARFCN=1675
[...]
```

Note: If the Android SDK is installed anywhere else, you can use the *-s* parameter to specify its directory.

Speed-up the passive scan
---------------------------

When looking for operators, an AT command is sent to the modem. If you want to speed-up the scanning, you can hardcoded the operators to the following file `cache/operators.json`:

```
{
    "20801": "Orange",
    "20810": "F SFR", 
    "20815": "Free",
    "20820": "F-Bouygues Telecom"
}
```

Only the MCC/MNC codes are inmportant. Then you can re-launch the tool as follows:

```
$ sudo python modmobmap.py -o   
=> Requesting a list of MCC/MNC. Please wait, it may take a while...
Found 4 operators in cache, you choose to reuse them.
Found 4 operator(s)
{u'20810': u'F SFR', u'20820': u'F-Bouygues Telecom', u'20815': u'Free', u'20801': u'Orange'} 
[+] Unregistered from current PLMN
[+] New cell detected [CellID/PCI-DL_freq  (XXXX-10614)]
 Network type=3G
 PLMN=208-10
 Band=1
 Downlink UARFCN=10614
 Uplink UARFCN=9664
[...]
[+] New cell detected [CellID/PCI-DL_freq  (XXX-3501)]
 Network type=4G
 PLMN=208-20
 Band=8
 Downlink EARFCN=3501
[...]
[+] Unregistered from current PLMN
=> Changing MCC/MNC for: 20815
[+] New cell detected [CellID/PCI-DL_freq  (XXX-2825)]
 Network type=4G
 PLMN=208-15
 Band=7
 Downlink EARFCN=2825
[...]
=> Changing MCC/MNC for: 20801
[+] New cell detected [CellID/PCI-DL_freq  (XXXXX-3011)]
 Network type=3G
 PLMN=208-1
 Band=8
 Downlink UARFCN=3011
 Uplink UARFCN=2786
[...]
```

Note we have been able to detect other cells the AT command *AT+COPS* did not returned.

A complet list of MCC and MNC codes could be retrieved anywhere on internet and in Wikipedia: https://en.wikipedia.org/wiki/Mobile_country_code

Focusing some operators
------------------------

It is possible to tell *Modmobmap* to focus only on specific operators with the *-m* argument:

```
$ sudo python modmobmap.py -n 20801
=> Manual MCC/MNC processing...
Found 1 operator(s)
{'20801': '20801'} 
[...]
=> Changing MCC/MNC for: 20801
[+] New cell detected [CellID/PCI-DL_freq  (XXX-1675)]
 Network type=4G
 PLMN=208-01
 Band=3
 Downlink EARFCN=1675
[+] New cell detected [CellID/PCI-DL_freq  (XXXXX-3011)]
 Network type=3G
 PLMN=208-1
 Band=8
 Downlink UARFCN=3011
 Uplink UARFCN=2786
=> Changing network type for 3G only
[+] New cell detected [CellID/PCI-DL_freq  (XXXXX-2950)]
 Network type=3G
 PLMN=208-1
 Band=8
 Downlink UARFCN=2950
 Uplink UARFCN=2725
```

Using Modmobmap with xgoldmon
------------------------------

With XGold modems, the use of xgoldmon will be required. But for now, only the fork for *Modmobmap* works to retrieve exact information of cells via the DIAG interface, and could be downloaded at: https://github.com/FlUxIuS/xgoldmon

Then after compiling, the tool *xgoldmon* could be started using the *-m* parameter like this:

```
sudo ./xgoldmon -t s3 -m /dev/ttyACM1
```

This will create a FIFO file that will be requested by Modmobmap later:

```
$ ls
celllog.fifo  Makefile   screenshot-mtsms-while-in-a-call.png  xgoldmon
```

Then we can start running *Modmobmap* as follows precising the AT serial interface (*/dev/ttyACM0*) and the fifo file created by *xgoldmon* (*<xgoldmonpath/celllog.fifo*):

```
$ sudo python3 modmobmap.py -f /<xgoldmon path>/celllog.fifo -m xgoldmod -a /dev/ttyACM0  -o
=> Requesting a list of MCC/MNC. Please wait, it may take a while...
Found 4 operators in cache, you choose to reuse them.
Found 4 operator(s)
{'20801': 'Orange', '20810': 'F SFR', '20815': 'Free', '20820': 'F-Bouygues Telecom'} 
[+] New cell detected [CellID/PCI-DL_freq  (0x7XXXX-65535)]
 Network type=3G
 PLMN=208-1
 Downlink UARFCN=65535
 Uplink UARFCN=2850
[+] Unregistered from current PLMN
[+] New cell detected [CellID/PCI-DL_freq  (0x7XXXX-3011)]
 Network type=3G
 PLMN=208-1
 Downlink UARFCN=3011
 Uplink UARFCN=2786
[...]
[+] Unregistered from current PLMN
=> Changing MCC/MNC for: 20810
[+] New cell detected [CellID/PCI-DL_freq  (0x3XXXXX-3075)]
 Network type=3G
 PLMN=208-10
 Downlink UARFCN=3075
 Uplink UARFCN=2850
[...]
 ```

Note that retrieving results from AT+COPS command could take a lot of time and sometime would need to restart the tool. If the tool is blocked on the operator retrieving step, please use cached or targeted operators features instead.

Saving results
---------------

The process could be stopped any time and results are save when killing the process with a keyboard interrupt signal:

```
[...]
^C[+] Cells save as cells_1528738901.json
```
