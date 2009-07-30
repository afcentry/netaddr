#-----------------------------------------------------------------------------
#   Copyright (c) 2008-2009, David P. D. Moss. All rights reserved.
#
#   Released under the BSD license. See the LICENSE file for details.
#-----------------------------------------------------------------------------
"""A basic implementation of RFC 1924 ;-)"""

from netaddr.core import AddrFormatError
from netaddr.ip import IPAddress

#-----------------------------------------------------------------------------
def chr_range(low, high):
    """Returns all characters between low and high chars."""
    return [chr(i) for i in range(ord(low), ord(high)+1)]

#: Base 85 integer index to character lookup table.
BASE_85 = chr_range('0', '9') + chr_range('A', 'Z') + chr_range('a', 'z') + \
    ['!', '#', '$', '%', '&', '(',')', '*', '+', '-',';', '<', '=', '>',
     '?', '@', '^', '_','`', '{', '|', '}', '~']

#: Base 85 digit to integer lookup table.
BASE_85_DICT = dict(zip(BASE_85, range(0, 86)))

#-----------------------------------------------------------------------------
def ipv6_to_base85(addr):
    """Convert a regular IPv6 address to base 85."""
    ip = IPAddress(addr)
    int_val = int(ip)

    remainder = []
    while int_val > 0:
        remainder.append(int_val % 85)
        int_val /= 85

    #print '-'.join([str(w) for w in reversed(remainder)])
    return ''.join([BASE_85[w] for w in reversed(remainder)])

#-----------------------------------------------------------------------------
def base85_to_ipv6(addr):
    """
    Convert a base 85 IPv6 address to its hexadecimal format.
    """
    tokens = list(addr)

    if len(tokens) != 20:
        raise AddrFormatError('Invalid base 85 IPv6 addess: %r' % addr)

    result = 0
    for i, num in enumerate(reversed(tokens)):
        num = BASE_85_DICT[num]
        result += (num * 85 ** i)

    ip = IPAddress(result, 6)

    return str(ip)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    ip_addr = '1080::8:800:200c:417a'
    print ip_addr
    base85 = ipv6_to_base85(ip_addr)
    print base85
    print base85_to_ipv6(base85)
