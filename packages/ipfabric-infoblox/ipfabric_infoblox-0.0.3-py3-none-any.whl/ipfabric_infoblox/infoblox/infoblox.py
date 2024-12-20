import csv
from io import StringIO
from ipaddress import ip_interface
from ipaddress import ip_network
from time import sleep
from typing import Any
from urllib.parse import urljoin

from httpx import Client
from pydantic import BaseModel, PrivateAttr
from pytricia import PyTricia
from requests import Session

from ipfabric_infoblox.config import Configuration
from ipfabric_infoblox.ipf_models.managed_ip import Export
from .models import View, Container, Network, Log

NETWORK_FIELDS = [
    "network_container",
    "conflict_count",
    "dynamic_hosts",
    "static_hosts",
    "total_hosts",
    "unmanaged_count",
]
DISCOVERY_FIELDS = ["csv_file_name", "scheduled_run", "state", "status", "warning"]


class Infoblox(BaseModel):
    config: Configuration
    _client: Client = PrivateAttr(None)
    _views: dict[str, View] = PrivateAttr(None)
    _default_view: str = PrivateAttr(None)
    _session: Session = PrivateAttr(None)
    _base_url: str = PrivateAttr(None)

    # TODO IPv6

    def model_post_init(self, __context: Any) -> None:
        self._client = Client(
            base_url=self.config.infoblox.host,
            auth=(self.config.infoblox.username, self.config.infoblox.password),
            verify=self.config.infoblox.verify_ssl,
            headers={"Content-Type": "application/json"},
        )
        self._session = Session()
        self._session.verify = self.config.infoblox.verify_ssl
        self._session.auth = (self.config.infoblox.username, self.config.infoblox.password)
        resp = self._client.get("wapi/v1.0/?_schema")
        resp.raise_for_status()
        version = max(resp.json()["supported_versions"])  # TODO: Which versions to do we allow?
        self._base_url = f"{self.config.infoblox.host}/wapi/v{version}/"
        self._client.base_url = self._base_url
        self._views = {view["name"]: View(**view) for view in self.ib_pager("networkview")}
        self._default_view = next(view.name for view in self._views.values() if view.is_default)

    @property
    def ib_default_view(self) -> str:
        return self._default_view

    @property
    def views(self) -> dict[str, View]:
        return self._views

    def ib_pager(self, url: str, params: dict = None) -> list[dict]:
        url = url.replace(":", "%3A")
        params = params or {}
        params.update({"_max_results": 1000, "_paging": 1, "_return_as_object": 1})
        resp = self._client.get(url, params=params)
        resp.raise_for_status()
        r_json = resp.json()
        data, next_page_id = r_json["result"], r_json.get("next_page_id", None)
        while next_page_id:
            params["_page_id"] = next_page_id
            resp = self._client.get(url, params=params)
            resp.raise_for_status()
            r_json = resp.json()
            data.extend(r_json["result"])
            next_page_id = r_json.get("next_page_id", None)
        return data

    @staticmethod
    def ip_version(ip: str) -> int:
        return ip_network(ip).version

    def containers(self, view: str = None) -> list[Container]:
        return [
            Container(**_)
            for _ in self.ib_pager(
                "networkcontainer",
                params={"network_view": view or self.ib_default_view},
            )
        ]

    def containers_pyt(self, view: str = None):
        pyt = PyTricia()
        for container in self.containers(view):
            if self.ip_version(container.network) == 4:
                pyt[container.network] = container
        return pyt

    def networks(self, view: str = None) -> list[Network]:
        return [
            Network(**_)
            for _ in self.ib_pager(
                "network",
                params={
                    "network_view": view or self.ib_default_view,
                    "_return_fields+": NETWORK_FIELDS,
                },
            )
        ]

    def networks_pyt(self, view: str = None):
        pyt = PyTricia()
        for network in self.networks(view):
            if self.ip_version(network.network) == 4:
                pyt[network.network] = network
        return pyt

    @staticmethod
    def create_csv(logs: list[Log], comment: str = ""):
        output = StringIO()
        csv_writer = csv.writer(output, dialect="excel", quoting=csv.QUOTE_ALL)
        csv_writer.writerow(["header-network", "address*", "netmask*", "comment", "network_view", "IMPORT-ACTION"])
        for log in logs:
            ip = ip_interface(log.network)
            csv_writer.writerow(
                [
                    "network",
                    str(ip.network.network_address),
                    str(ip.network.netmask),
                    comment,
                    log.network_view,
                    "IO" if log.has_parent_network else "I",
                ]
                # ["network", str(ip.network.network_address), str(ip.network.netmask), comment, log.network_view]
            )
        return output

    @staticmethod
    def create_ip_csv(ips: list[Export]):
        output = StringIO()
        csv_writer = csv.DictWriter(
            output, dialect="excel", quoting=csv.QUOTE_ALL, fieldnames=ips[0].model_fields.keys()
        )
        csv_writer.writeheader()
        for ip in ips:
            csv_writer.writerow(ip.model_dump())
        return output

    def _upload_init(self, csv_data: StringIO, filename: str = "ipfabric.csv"):
        # valid filename, only alphanumeric characters, underscores and periods are supported
        resp = self._client.post(
            urljoin(self._base_url, "fileop"), params={"_function": "uploadinit"}, json={"filename": filename}
        )
        resp.raise_for_status()
        data = resp.json()
        upload_resp = self._session.post(data["url"], files={"file": csv_data.getvalue()})
        upload_resp.raise_for_status()
        return data

    def csv_upload(self, csv_data: StringIO):
        data = self._upload_init(csv_data, "ipfabric.csv")
        import_resp = self._client.post(
            "fileop",
            params={"_function": "csv_import"},
            json={"operation": "CUSTOM", "token": data["token"], "on_error": "CONTINUE"},
        )
        import_resp.raise_for_status()
        csv_ref = import_resp.json()["csv_import_task"]["_ref"]
        while (resp := self._client.get(csv_ref).json()) and resp["status"] not in ["COMPLETED", "FAILED", "STOPPED"]:
            sleep(5)
            # TODO: How long do we wait?
        return resp

    def csv_discovery_upload(self, csv_data: StringIO, view: str):
        task_name = f"ipfDiscovery_{view}"
        data = self._upload_init(csv_data, f"{task_name}.csv")
        import_resp = self._client.post(
            "fileop",
            params={"_function": "setdiscoverycsv"},
            json={"merge_data": True, "token": data["token"], "network_view": view},
        )
        import_resp.raise_for_status()
        params = {"_return_fields+": DISCOVERY_FIELDS}
        # params = {"_return_fields+": DISCOVERY_FIELDS, "discovery_task_oid": "current"}
        disc_resp = self._client.get("discoverytask", params=params)
        disc_resp.raise_for_status()
        task = {_["csv_file_name"]: _["_ref"] for _ in disc_resp.json()}.get(task_name)
        while (resp := self._client.get(task, params=params).json()) and resp["state"] not in ["COMPLETE", "ERROR"]:
            sleep(5)
        # print(resp["status"])  # TODO: Logging
        return True
