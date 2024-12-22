from typing import Iterable

from routelookup import ipmath
from routelookup.api import RouteTable, AddrHandler
from routelookup.compat import net_to_tuple
from routelookup.typehints import A, N, T, IPVersion


class BaseRouteTable(RouteTable[A, N, T]):
    def __init__(self, addr_handler: AddrHandler[A, N]):
        self.addr_handler = addr_handler
        self.table: dict[tuple[int, int, IPVersion], T] = {}

    def __setitem__(self, prefix: A | N | str, value: T) -> None:
        self.table[net_to_tuple(prefix)] = value

    def __getitem__(self, prefix: A | N | str) -> T:
        key = net_to_tuple(prefix)
        try:
            return self.table[key]
        except KeyError:
            pass
        net, prefixlen, version = key
        for prefixlen_new in range(prefixlen - 1, -1, -1):
            try:
                return self.table[
                    ipmath.with_prefixlen(net, prefixlen_new, version), prefixlen_new, version
                ]
            except KeyError:
                pass
        raise KeyError(prefix)

    def __delitem__(self, prefix: A | N | str) -> None:
        del self.table[net_to_tuple(prefix)]

    def remove(self, prefix: A | N | str) -> None:
        self.table.pop(net_to_tuple(prefix), None)

    def lookup_worst(self, prefix: A | N | str) -> T:
        net, prefixlen, version = net_to_tuple(prefix)
        for prefixlen_new in range(prefixlen + 1):
            try:
                return self.table[
                    ipmath.with_prefixlen(net, prefixlen_new, version), prefixlen_new, version
                ]
            except KeyError:
                pass
        raise KeyError(prefix)

    def lookup_range(self, prefix: A | N | str) -> Iterable[tuple[N, T]]:
        net, prefixlen, version = net_to_tuple(prefix)
        return (
            (self.addr_handler.build_net(table_net, table_prefixlen, version), value)
            for (table_net, table_prefixlen, version), value in self.table.items()
            if ipmath.is_subnet(table_net, net, prefixlen, version)
        )

    def items(self) -> Iterable[tuple[N, T]]:
        return (
            (self.addr_handler.build_net(net, prefixlen, version), v)
            for (net, prefixlen, version), v in self.table.items()
        )

    def __len__(self) -> int:
        return len(self.table)

    def __contains__(self, prefix: A | N | str) -> bool:
        key = net_to_tuple(prefix)
        if key in self.table:
            return True
        net, prefixlen, version = key
        return any((ipmath.with_prefixlen(net, prefixlen_new, version), prefixlen_new, version) in self.table for prefixlen_new in range(prefixlen - 1, -1, -1))


# class BaseRouteTable(RouteTable[N, T]):
#     def __init__(self, addrhandler: AddrHandler[N]):
#         self.table: dict[tuple[int, int], T] = {}
#         self.addrhandler = addrhandler
#
#     def __setitem__(self, prefix: A | N | str, value: T) -> None:
#         if isinstance(prefix, str):
#             prefix = self.addrhandler.str_to_net(prefix)
#         self.table[self.addrhandler.net_to_tuple(prefix)] = value
#
#     def __getitem__(self, prefix: A | N | str) -> T:
#         if isinstance(prefix, str):
#             prefix = self.addrhandler.str_to_net(prefix)
#         key = self.addrhandler.net_to_tuple(prefix)
#         try:
#             return self.table[key]
#         except KeyError:
#             pass
#         net, mask = key
#         mask_len = ipmath.prefixlen(mask)
#         for mask_new in (ipmath.get_mask(n) for n in range(mask_len - 1, -1, -1)):
#             try:
#                 return self.table[ipmath.with_mask(net, mask_new), mask_new]
#             except KeyError:
#                 pass
#         raise KeyError(prefix)
#
#     def __delitem__(self, prefix: A | N | str) -> None:
#         if isinstance(prefix, str):
#             prefix = self.addrhandler.str_to_net(prefix)
#         del self.table[self.addrhandler.net_to_tuple(prefix)]
#
#     def items(self) -> Iterable[tuple[N, T]]:
#         for k, v in self.table.items():
#             yield self.addrhandler.build_net(*k), v
