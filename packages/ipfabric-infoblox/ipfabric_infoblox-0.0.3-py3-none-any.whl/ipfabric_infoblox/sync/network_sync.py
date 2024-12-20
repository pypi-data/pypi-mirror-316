import re
from typing import Any

from pydantic import BaseModel, PrivateAttr, Field

from ipfabric_infoblox.config import Configuration, DEFAULT_VRF
from ipfabric_infoblox.config.network_view import NetworkView
from ipfabric_infoblox.ipf_models.managed_networks import ManagedNetworks, ManagedNetwork


class Map(BaseModel):
    include: set[NetworkView] = Field(default_factory=set)
    exclude: set[NetworkView] = Field(default_factory=set)


class NetworkSync(BaseModel):
    ipf: Any
    config: Configuration
    _networks: ManagedNetworks = PrivateAttr(None)
    _site_map: dict[str, Map] = PrivateAttr(default_factory=dict)
    _vrf_map: dict[str, Map] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        self._networks = self._get_ipv4_nets()
        self._site_map = {_: Map(**self._mapping(_, "sites")) for _ in self._networks.sites}
        self._vrf_map = {_: Map(**self._mapping(_, "vrfs")) for _ in self._networks.vrfs}
        self.map_net_view()
        self.map_vrf_view()
        self.map_site_view()
        self.map_default_view()

    @property
    def networks(self) -> ManagedNetworks:
        return self._networks

    @staticmethod
    def _calculate_vrf(vrf: str, dev: dict) -> str:
        if dev["vendor"] not in DEFAULT_VRF:
            default_vrf = ""
        elif dev["family"] not in DEFAULT_VRF[dev["vendor"]]:
            default_vrf = DEFAULT_VRF[dev["vendor"]].get(None, "")
        else:
            default_vrf = DEFAULT_VRF[dev["vendor"]][dev["family"]]
        return vrf if vrf != default_vrf else ""

    def _get_ipv4_nets(self) -> ManagedNetworks:
        devs = {_["sn"]: _ for _ in self.ipf.inventory.devices.all(columns=["sn", "vendor", "family"])}

        networks = set()
        vrf_map = self.config.ipfabric.mapped_vrfs
        for net in self.ipf.technology.addressing.managed_ip_ipv4.all(
            columns=["siteName", "net", "vrf", "sn"], filters={"net": ["empty", False]}
        ):
            net["vrf"] = self._calculate_vrf(net["vrf"], devs[net["sn"]])
            net["mapped_vrf"] = net["vrf"]
            if net["vrf"] in vrf_map or net["vrf"].lower() in vrf_map:
                net["mapped_vrf"] = vrf_map[net["vrf"]] if net["vrf"] in vrf_map else vrf_map[net["vrf"].lower()]

            networks.add(ManagedNetwork(**net))
        return ManagedNetworks(networks=list(networks))

    @staticmethod
    def _map(value, test) -> bool:
        if (
            (test.regex and re.match(test.value, value, flags=re.IGNORECASE if test.ignore_case else 0))
            or (test.ignore_case and test.value.lower() == value.lower())
            or test.value == value
        ):
            return True
        return False

    def _mapping(self, value: str, attr: str) -> dict[str, set[NetworkView]]:
        include, exclude = set(), set()
        for view in self.config.network_views:
            for inc in getattr(view.include, attr):
                if self._map(value, inc):
                    include.add(view)
            for exc in getattr(view.exclude, attr):
                if self._map(value, exc):
                    exclude.add(view)
        return {"include": include - exclude, "exclude": exclude}

    def _is_site_included(self, site: str, view: str) -> bool:
        if view not in self._site_map[site].exclude and (
            (self._site_map[site].include and view in self._site_map[site].include) or not self._site_map[site].include
        ):
            return True
        return False

    def _is_vrf_included(self, vrf: str, view: str) -> bool:
        if (
            vrf in self._vrf_map
            and view not in self._vrf_map[vrf].exclude
            and ((self._vrf_map[vrf].include and view in self._vrf_map[vrf].include) or not self._vrf_map[vrf].include)
        ):
            return True
        return False

    @staticmethod
    def _is_net_allowed(net, view: NetworkView) -> bool:
        return True if net in view.pyt and view.pyt[net] == "INCLUDE" else False

    @staticmethod
    def _check_views(network: ManagedNetwork, tmp: set[str], error_gt_1: str, error_eq_0: str, success: str):
        if len(tmp) == 1:
            network.net_view = tmp.pop()
            network.error.multiple_views, network.error.no_matching_view = False, False
            network.success.network_view = success
        elif len(tmp) > 1:
            network.error.multiple_views = True
            network.error.message.append(error_gt_1)
        elif not tmp:
            network.error.no_matching_view = True
            network.error.message.append(error_eq_0)
        return network

    def _if_included(self, view: NetworkView, network: ManagedNetwork) -> bool:
        if (
            self._is_site_included(network.site_name, view.name)
            and self._is_vrf_included(network.vrf, view.name)
            and self._is_net_allowed(network.network, view)
        ):
            return True
        return False

    def map_net_view(self):
        for network in self._networks.networks:
            net = network.network
            if net not in self.config.pyt:
                continue
            tmp = set()
            for view in self.config.pyt[net]:
                if self._if_included(self.config.view_dict[view], network):
                    tmp.add(view)
            self._check_views(
                network,
                tmp,
                f"Multiple matching Network Views based on Network Config found: {','.join(tmp)}",
                "No matching Network Views found based on Network Config will continue with VRF, Site, and Default.",
                "Matched Network based on Network Mapping.",
            )

    def _map_view(self, mapping, attr, error_gt_1: str, error_eq_0: str, success: str):
        for network in self._networks.networks:
            if network.net_view:
                continue
            tmp = set()
            for view in mapping[getattr(network, attr)].include:
                if self._if_included(view, network):
                    tmp.add(view.name)
            self._check_views(network, tmp, f"{error_gt_1}{','.join(tmp)}", error_eq_0, success)

    def map_vrf_view(self):
        self._map_view(
            self._vrf_map,
            "vrf",
            "Multiple matching Network Views based on VRF Config found: ",
            "No matching Network Views found based on VRF Config will continue with Site and Default.",
            "Matched Network based on VRF Mapping.",
        )

    def map_site_view(self):
        self._map_view(
            self._site_map,
            "site_name",
            "Multiple matching Network Views based on Site Name Config found: ",
            "No matching Network Views found based on Site Name Config will continue with Default.",
            "Matched Network based on Site Name Mapping.",
        )

    def map_default_view(self):
        default = self.config.default_view
        for network in self._networks.networks:
            if network.net_view:
                continue
            if not self.config.default_view:
                network.error.no_matching_view = True
                network.error.message.append("Network did not match any rules and no default assigned.")
            tmp = set()
            if (
                self._is_site_included(network.site_name, default.name)
                and self._is_vrf_included(network.vrf, default.name)
                and self._is_net_allowed(network.network, default)
            ):
                tmp.add(default)
                network.net_view = default
                network.error.multiple_views, network.error.no_matching_view = False, False
                network.success.network_view = "Matched Network based on Default Mapping."
            else:
                network.error.no_matching_view = True
                network.error.message.append("Network did not match any rules and excluded by default.")
