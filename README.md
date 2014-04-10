python-netgear
==============

API written in python download/upload configuration of NetGear switch

Installation
------------

1. Fill the authentication credentials in `netgear.conf`

Usage
-----

### `getconfig`

Retrieve the switch configuration

    usage: getconfig [-h] [-o OUTPUTFILE] [-D] [-v]
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUTFILE, --outputfile OUTPUTFILE
                            Destination file
      -D, --debug           Debug mode
      -v, --version         Display version

### `sendconfig`

Send configuration file to the switch & apply changes

    usage: sendconfig [-h] [-D] [-v] configfile
    
    positional arguments:
      configfile     Switch configuration file
    
    optional arguments:
      -h, --help     show this help message and exit
      -D, --debug    Debug mode
      -v, --version  Display version
    
