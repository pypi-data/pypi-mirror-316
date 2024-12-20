import csv
from pathlib import Path
from typing import Any

from ipfabric import IPFClient
from pydantic import BaseModel, PrivateAttr

from ipfabric_infoblox.config import Configuration
from ipfabric_infoblox.infoblox.models import Log, Field
from ipfabric_infoblox.ipf_models.managed_ip import ManagedIP
from ipfabric_infoblox.sync.ip_sync import IPSync
from ipfabric_infoblox.sync.network_sync import NetworkSync


class Sync(BaseModel):
    config: Configuration
    logs: list[Log] = Field(default_factory=list)
    _ipf: IPFClient = PrivateAttr(None)
    _network_sync: NetworkSync = PrivateAttr(None)
    _ip_sync: list[ManagedIP] = PrivateAttr(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        self._ipf = IPFClient(
            base_url=self.config.ipfabric.base_url,
            auth=(
                self.config.ipfabric.token
                if self.config.ipfabric.token
                else (self.config.ipfabric.username, self.config.ipfabric.password)
            ),
            verify=self.config.ipfabric.verify,
            timeout=self.config.ipfabric.timeout,
            snapshot_id=self.config.ipfabric.snapshot_id,
        )
        self._network_sync = NetworkSync(ipf=self._ipf, config=self.config)
        self._ip_sync = IPSync(ipf=self._ipf).build()

    @property
    def network_sync(self) -> NetworkSync:
        return self._network_sync

    @property
    def ip_sync(self) -> list[ManagedIP]:
        return self._ip_sync

    def export_logs_to_csv(self, file_path: str) -> None:
        file_path = Path(file_path)
        with file_path.open(mode="w", newline="") as csv_file:
            fieldnames = list(Log.model_json_schema()["properties"].keys())
            computed_fields = [
                "parent_network_has_hosts",
                "has_parent_network",
                "has_network_match",
                "network_is_container",
                "failed",
                "status",
                "skipped",
                "create",
            ]
            fieldnames.extend(computed_fields)
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for log in self.logs:
                log_dict = log.model_dump()
                writer.writerow(log_dict)
