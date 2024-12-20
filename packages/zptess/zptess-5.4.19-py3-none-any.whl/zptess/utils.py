# ----------------------------------------------------------------------
# Copyright (c) 2022
#
# See the LICENSE file for details
# see the AUTHORS file for authors
# ----------------------------------------------------------------------

#--------------------
# System wide imports
# -------------------

import re

from zptess import SERIAL_PORT_PREFIX, TEST_SERIAL_PORT, TEST_BAUD
from zptess import TEST_IP, TEST_TCP_PORT, TEST_UDP_PORT


# ------------------------
# Module Utility Functions
# ------------------------

def chop(string, sep=None):
    '''Chop a list of strings, separated by sep and 
    strips individual string items from leading and trailing blanks'''
    chopped = [ elem.strip() for elem in string.split(sep) ]
    if len(chopped) == 1 and chopped[0] == '':
    	chopped = []
    return chopped



def valid_ip_address(ip):
    '''Validate an IPv4 address returning True or False'''
    return [ 0 <= int(x) < 256 for x in re.split(r'\.', re.match(r'^\d+\.\d+\.\d+\.\d+$',ip).group(0))].count(True) == 4


def mkendpoint(value, 
    default_ip=TEST_IP, 
    default_tcp_port=TEST_TCP_PORT, 
    default_udp_port=TEST_UDP_PORT , 
    default_serial_port=TEST_SERIAL_PORT, 
    default_baud=TEST_BAUD):
    '''
    Utility to convert command line values to serial or tcp endpoints
    tcp
    tcp::<port>
    tcp:<ip>
    tcp:<ip>:<port>
    udp
    udp::<port>
    udp:<ip>
    udp:<ip>:<port>
    serial
    serial::<baud>
    serial:<serial_port>
    serial:<serial_port>:<baud>

    '''
    parts = [elem.strip() for elem in value.split(':') ]
    length = len(parts)
    if length < 1 or length > 3:
        raise argparse.ArgumentTypeError("Invalid endpoint format {0}".format(value))
    proto = parts[0]
    if proto == "tcp":
        if length == 1:
            ip   = str(default_ip)
            port = str(default_tcp_port)
        elif length == 2:
            ip   = parts[1]
            port = str(default_tcp_port)
        elif valid_ip_address(parts[1]):
            ip   = parts[1]
            port = parts[2]
        else:
            ip   = str(default_ip)
            port = parts[2]
        result = proto + ':' + ip + ':' + port
    elif proto == "serial":
        if length == 1:
            serial = SERIAL_PORT_PREFIX + str(default_serial_port)
            baud   = str(default_baud)
        elif length == 2:
            serial = SERIAL_PORT_PREFIX + str(parts[1])
            baud   = str(default_baud)
        elif parts[1] != '':
            serial = SERIAL_PORT_PREFIX + str(parts[1])
            baud   = parts[2]
        else:
            serial = SERIAL_PORT_PREFIX + str(default_serial_port)
            baud   = parts[2]
        result = proto + ':' + serial + ':' + baud
    elif proto == "udp":
        if length == 1:
            ip   = str(default_ip)
            port = str(default_udp_port)
        elif length == 2:
            ip   = parts[1]
            port = str(default_udp_port)
        elif valid_ip_address(parts[1]):
            ip   = parts[1]
            port = parts[2]
        else:
            ip   = str(default_ip)
            port = parts[2]
        result = proto + ':' + ip + ':' + port
    else:
        raise argparse.ArgumentTypeError("Invalid endpoint prefix {0}".format(parts[0]))
    return result


  
__all__ = [
	"chop",
    "valid_ip_address",
    "mkendpoint",
]
