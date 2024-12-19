"""A collection of network utility functions."""

# Copyright (C) 2024  Stefano Cuizza

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import Literal

from scapy.arch import get_if_addr, get_if_hwaddr
from scapy.config import conf


def get_local_ip() -> str:
    """Returns the IP address of the local machine."""

    return get_if_addr(conf.iface)


def get_mac() -> str:
    """Returns the MAC address of the local machine."""

    return get_if_hwaddr(conf.iface)


def get_default_gateway() -> str:
    """Returns the IP address of the default gateway."""

    return conf.route.route('0.0.0.0')[2]


def mac_dec_to_hex_notation(mac_address: int, separator: Literal[':', '-'] = ':') -> str:
    """Translates a decimal MAC address in its human-readable representation.

    Args:
        mac_address:
            the MAC address to translate.
        separator:
            character to use as a separator.
    """

    mac_hex = f'{mac_address:012x}'
    return separator.join(mac_hex[i:i + 2] for i in range(0, len(mac_hex), 2))
