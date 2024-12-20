from typing import Optional

from pydantic import BaseModel, Field, computed_field

from ipfabric_infoblox.ipf_models import ManagedNetwork


class Ref(BaseModel):
    ref: str = Field(alias="_ref")
    comment: Optional[str] = None


class View(Ref, BaseModel):
    name: str
    is_default: bool


class Container(Ref, BaseModel):
    network: str
    network_view: str


class Network(Container, BaseModel):
    network_container: str
    conflict_count: int
    dynamic_hosts: int
    static_hosts: int
    total_hosts: int
    unmanaged_count: int

    @property
    def has_hosts(self) -> bool:
        return (
            self.total_hosts + self.conflict_count + self.dynamic_hosts + self.static_hosts + self.unmanaged_count
        ) > 0


class Log(BaseModel):
    network: str
    network_view: str
    create_containerless_nets: bool = False
    split_networks: bool = False
    smallest_v4_subnet: int = 31
    ipf_networks: set[ManagedNetwork]
    network_container: Optional[Container] = None
    parent_network: Optional[Network] = None
    network_match: Optional[Network] = None
    created_network: Optional[Network] = None
    has_child_network: bool = False
    failure: Optional[str] = None
    skip_reason: Optional[str] = None

    def __str__(self):
        return f"{self.network} - {self.network_view}"

    def __hash__(self):
        return hash(str(self))

    @computed_field
    @property
    def has_parent_network(self) -> bool:
        return self.parent_network is not None

    @computed_field
    @property
    def parent_network_has_hosts(self) -> bool:
        return self.parent_network.has_hosts if self.parent_network else False

    @computed_field
    @property
    def network_is_container(self) -> bool:
        return self.network_container.network == self.network if self.network_container else False

    @computed_field
    @property
    def has_network_match(self) -> bool:
        return self.network_match is not None

    @computed_field
    @property
    def skipped(self) -> bool:
        return self.skip_reason is not None

    @computed_field
    @property
    def failed(self) -> bool:
        return self.failure is not None

    @computed_field
    @property
    def create(self) -> bool:
        return not self.failed and not self.skipped and not self.has_network_match

    @computed_field
    @property
    def status(self) -> str:
        """Dynamically computed status based on log properties."""
        if self.failed:
            return "failed"
        elif self.skipped:
            return "skipped"
        elif self.create:
            return "create"
        elif self.has_network_match:
            return "exists"
        return "unknown"
