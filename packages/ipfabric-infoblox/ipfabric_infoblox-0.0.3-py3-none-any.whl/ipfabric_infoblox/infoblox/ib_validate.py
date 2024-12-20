from collections import defaultdict
from ipaddress import ip_network
from typing import Any

from pydantic import BaseModel
from pytricia import PyTricia

from ipfabric_infoblox.config.network_view import NetworkView
from ipfabric_infoblox.ipf_models import ManagedNetwork, ManagedIP, Export
from ipfabric_infoblox.sync.sync import Sync
from .models import Log


class NetworkValidation(BaseModel):
    view_config: NetworkView
    network_view: str
    networks_pyt: Any
    containers_pyt: Any
    sync: Sync

    def _copy_pyt(self, network) -> PyTricia:
        if self.networks_pyt.has_key(network):
            return self.networks_pyt
        else:
            tmp = PyTricia()
            [tmp.insert(_, self.networks_pyt[_]) for _ in self.networks_pyt]
            tmp.insert(network, network)
            return tmp

    def _validate_network(self, log: Log, policy: str) -> Log:
        network = log.network
        ip = ip_network(network)
        if ip.version == 4 and ip.prefixlen > log.smallest_v4_subnet:
            log.skip_reason = f"Skipping IPF subnet '{network}' because mask is greater than `smallest_v4_subnet={log.smallest_v4_subnet}`."
        elif self._copy_pyt(network).children(network):
            log.has_child_network = True
            log.failure = f"Failed for IPF subnet '{network}' because IB has children network(s)."
        elif network in self.networks_pyt and self.networks_pyt[network].has_hosts:
            log.parent_network = self.networks_pyt[network]
            log.failure = f"Failed for IPF subnet '{network}' because parent IB Network '{self.networks_pyt[network].network}' has hosts."
        elif network in self.networks_pyt and not log.split_networks:
            log.parent_network = self.networks_pyt[network]
            log.skip_reason = f"Skipping IPF subnet '{network}' under parent IB Network '{self.networks_pyt[network].network}' because `{policy}` is True and `split_networks` is False."
        elif network in self.networks_pyt:
            log.parent_network = self.networks_pyt[network]
        return log

    def validate_network(self, ipf_network: ManagedNetwork) -> Log:
        network = str(ipf_network.network)
        log = Log(
            network=network,
            network_view=self.network_view,
            create_containerless_nets=self.view_config.create_containerless_nets,
            split_networks=self.view_config.split_networks,
            smallest_v4_subnet=self.view_config.smallest_v4_subnet,
            ipf_networks={ipf_network},
        )
        if self.containers_pyt.has_key(network):
            log.network_container = self.containers_pyt[network]
            log.failure = (
                f"Failed for IPF subnet '{network}' because it is an IB Container '{log.network_container.network}'."
            )
        elif network in self.containers_pyt and self.networks_pyt.has_key(network):
            log.network_container = self.containers_pyt[network]
            log.network_match = self.networks_pyt[network]
        elif network in self.containers_pyt:
            log.network_container = self.containers_pyt[network]
            log = self._validate_network(log, "ib_create_network")
        elif self.networks_pyt.has_key(network):
            log.network_match = self.networks_pyt[network]
        elif not self.view_config.create_containerless_nets:
            log.skip_reason = f"Skipping IPF subnet '{network}' because `create_containerless_nets` is False."
        else:
            log = self._validate_network(log, "ib_create_container")

        self.sync.logs.append(log)
        return log


class FinalValidation(BaseModel):
    @staticmethod
    def _validate_logs(logs: set[Log]) -> set[Log]:
        pyt = PyTricia()
        skip, create = set(), set()
        for log in logs:
            if log.create:
                pyt[log.network] = log
            else:
                skip.add(log)

        for net in pyt:
            if pyt.parent(net) or pyt.children(net):
                pyt[net].failure = f"Failed for IPF subnet '{net}' because overlapping IP Fabric networks found."
            create.add(pyt[net])
        return skip | create

    def validate_logs(self, logs: list[Log], pyt_validate: bool = True) -> list[Log]:
        views = defaultdict(dict)
        for log in logs:
            if str(log) in views[log.network_view]:
                views[log.network_view][str(log)].ipf_networks.update(log.ipf_networks)
            else:
                views[log.network_view][str(log)] = log
        if not pyt_validate:
            return [log for logs in views.values() for log in logs.values()]

        final = list()
        for view, logs in views.items():
            tmp = {views[view][_] for _ in logs}
            final.extend(list(self._validate_logs(tmp)))
        return final

    def validate_ips(self, managed_ips: dict[str, list[ManagedIP]]) -> dict[str, list[Export]]:
        validated = {_: list() for _ in managed_ips}
        for view, ips in managed_ips.items():
            tmp = defaultdict(list)
            for ip in ips:
                tmp[ip.ip].append(ip)
            for ip, mips in tmp.items():
                if len(mips) == 1:
                    validated[view].append(mips[0].export())
                else:
                    validated[view].append(ManagedIP.join_ips(mips))
        return validated
