from ipaddress import IPv6Network, IPv6Address, IPv4Address, IPv4Network, ip_network

from routelookup.typehints import IPVersion

try:
    # noinspection PyUnresolvedReferences
    import netaddr

    def net_to_tuple(value) -> tuple[int, int, IPVersion]:
        if isinstance(value, netaddr.IPNetwork):  # todo ipaddress
            return int(value.network), value.prefixlen, value.version
        if isinstance(value, (IPv4Network, IPv6Network)):
            return int(value.network_address), value.prefixlen, value.version
        if isinstance(value, (IPv4Address, IPv6Address)):
            return int(value), value.max_prefixlen, value.version
        value = ip_network(value, strict=False)
        return int(value.network_address), value.prefixlen, value.version

except ImportError:

    def net_to_tuple(value) -> tuple[int, int, IPVersion]:
        if isinstance(value, (IPv4Network, IPv6Network)):
            return int(value.network_address), value.prefixlen, value.version
        if isinstance(value, (IPv4Address, IPv6Address)):
            return int(value), value.max_prefixlen, value.version
        value = ip_network(value, strict=False)
        return int(value.network_address), value.prefixlen, value.version
