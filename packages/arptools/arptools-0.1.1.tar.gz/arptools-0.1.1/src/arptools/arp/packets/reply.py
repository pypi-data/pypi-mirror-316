"""Provides functions to send ARP replies."""

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


from collections.abc import Callable
from typing import Optional

from scapy.layers.l2 import ARP, Ether
from scapy.packet import Packet
from scapy.plist import PacketList, QueryAnswer, SndRcvList
from scapy.sendrecv import srploop, srp

from . import _prn, _prnfail


def arp_reply(
        target_ip: str,
        ethernet_src: Optional[str] = None,
        ethernet_dst: Optional[str] = None,
        arp_hwsrc: Optional[str] = None,
        arp_psrc: Optional[str] = None,
        count: int = 0,
        interval: float = 1.0,
        verbose: Optional[int] = None,
        prn: Callable[[QueryAnswer], str | None] = _prn,
        prnfail: Callable[[Packet | PacketList | SndRcvList], str | None] = _prnfail,
) -> None:
    """Sends an ARP reply packet.

    Args:
        target_ip:
            the target IP of the ARP reply.
        ethernet_src:
            the source MAC address of the Ethernet frame.
        ethernet_dst:
            the destination MAC address of the Ethernet frame.
        arp_hwsrc:
            the hardware source address of the ARP packet.
        arp_psrc:
            the protocol source address of the ARP packet.
        count:
            how many packet to send.
        interval:
            time interval between packets (only used when count is 0).
        verbose:
            verbosity level.
        prn:
            function used to print packets that have received an answer.
        prnfail:
            function used to print packets that have not received an answer.
    """

    pkt = (
            Ether(dst=ethernet_dst, src=ethernet_src) /
            ARP(op='is-at', hwsrc=arp_hwsrc, psrc=arp_psrc, pdst=target_ip)
    )

    if count:
        _results, unanswered = srp(
            pkt if count == 1 else tuple(pkt for _ in range(count)),
            timeout=0,
            verbose=verbose,
        )

        if verbose != 0:
            if prn_results := prnfail(unanswered):
                print('', prn_results, sep='\n')

        return

    srploop(
        pkt,
        inter=interval,
        prn=prn,
        prnfail=prnfail,
        verbose=verbose,
    )
