import os
from collections import defaultdict
from typing import Annotated

import typer
import yaml
from rich.console import Console

from ipfabric_infoblox.config import Configuration
from ipfabric_infoblox.infoblox.ib_validate import NetworkValidation, FinalValidation
from ipfabric_infoblox.infoblox.infoblox import Infoblox
from ipfabric_infoblox.sync.sync import Sync

app = typer.Typer()
console = Console()

DEFAULT_LOG_FILE = "diff.csv"


def print_error_and_abort(message: str):
    console.print(f"Error: {message}", style="bold red")
    raise typer.Abort()


def load_yaml_config(config_file: typer.FileText) -> dict:
    try:
        config_data = yaml.safe_load(config_file)
        return config_data
    except yaml.YAMLError as exc:
        typer.echo(f"Error parsing YAML file: {exc}", err=True)
        raise typer.Exit(code=1)


def common_logic(config_file: typer.FileText, logging: bool):
    console.print(
        f"Comparing networks in [link={os.environ.get('IPF_URL')}]IP Fabric[/link] and [link={os.environ.get('IB_HOST')}]Infoblox[/link]",
        style="bold green",
    )
    config_data = load_yaml_config(config_file)
    config = Configuration(**config_data)
    sync = Sync(config=config)
    ib = Infoblox(config=config)
    for view in config.network_views:
        if view.name not in ib.views:
            raise ValueError(f"View {view.name} does not exists in IB.")
    views = {
        _.name: NetworkValidation(
            view_config=_,
            network_view=_.name,
            networks_pyt=ib.networks_pyt(_.name),
            containers_pyt=ib.containers_pyt(_.name),
            sync=sync,
        )
        for _ in config.network_views
    }
    validated_networks, matched_networks, ib_csv, ib_ip_csvs = [], [], None, None
    for network in sync.network_sync.networks.networks:
        if not network.success.network_view:
            console.print(f"Error: Network {network.network} failed to validate.", style="bold red")
            continue
        validated = views[network.net_view].validate_network(network)
        if validated.create:
            validated_networks.append(validated)
        if validated.has_network_match:
            matched_networks.append(validated)

    validated_networks = FinalValidation().validate_logs(
        logs=validated_networks
    )  # TODO: This fixes duplicate networks but now all the logging is screwed up
    matched_networks = FinalValidation().validate_logs(logs=matched_networks, pyt_validate=False)

    for log in sync.logs:
        console.print(f"    {log.network} - {log.status} {log.skip_reason if log.skip_reason else ''}")

    if logging:
        sync.export_logs_to_csv(DEFAULT_LOG_FILE)
        console.print(f"Logs exported to {DEFAULT_LOG_FILE}", style="bold green")

    create_nets = [_ for _ in validated_networks if _.create]
    if create_nets:
        console.print("Creating Infoblox Network CSV import CSV file.", style="bold green")
        ib_csv = ib.create_csv(logs=create_nets, comment="Synced from IP Fabric")

    ipf_nets = dict()
    for log in create_nets + matched_networks:
        for net in log.ipf_networks:
            site = ipf_nets.setdefault(net.site_name, dict())
            vrf = site.setdefault(net.vrf, dict())
            vrf[str(net.network)] = log

    validated_ip = defaultdict(list)
    for ip in sync.ip_sync:
        # TODO: What to do with /31 and /32
        log = ipf_nets.get(ip.siteName, {}).get(ip.vrf, {}).get(str(ip.net.network))
        if log:
            validated_ip[log.network_view].append(ip)
    validated_ip = FinalValidation().validate_ips(validated_ip)

    if validated_ip:
        console.print("Creating Infoblox IP Discovery CSV import CSV file.", style="bold green")
        ib_ip_csvs = {
            k: ib.create_ip_csv(v) for k, v in validated_ip.items() if views[k].view_config.managed_ip_discovery
        }

    return config, sync, ib, ib_csv, ib_ip_csvs


@app.command(name="diff")
def diff_cmd(
    config: Annotated[
        typer.FileText, typer.Option(help="YAML file with configuration default = config.yml")
    ] = "config.yml",
    logging: Annotated[bool, typer.Option(help="Say hi formally.")] = False,
):
    """Diff command to compare configurations."""
    common_logic(config, logging)


@app.command(name="sync")
def sync_cmd(
    config: Annotated[
        typer.FileText, typer.Option(help="YAML file with configuration default = config.yml")
    ] = "config.yml",
    logging: Annotated[bool, typer.Option(help="Say hi formally.")] = False,
):
    """Sync command to compare configurations."""
    config, _, ib, ib_csv, ib_ip_csvs = common_logic(config, logging)

    if not ib_csv:
        console.print("No networks to sync", style="bold red")
    else:
        data = ib.csv_upload(ib_csv)
        # TODO: Error checking of upload
    if not ib_ip_csvs:
        console.print("No IPs to sync", style="bold red")
    else:
        for view, ips in ib_ip_csvs.items():
            ib.csv_discovery_upload(ips, view)


if __name__ == "__main__":
    app()
