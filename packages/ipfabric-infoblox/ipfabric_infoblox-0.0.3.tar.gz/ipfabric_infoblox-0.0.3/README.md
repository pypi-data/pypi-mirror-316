# IP Fabric Infoblox Integration - BETA

## IP Fabric

[IP Fabric](https://ipfabric.io) is a vendor-neutral network assurance platform that automates the 
holistic discovery, verification, visualization, and documentation of 
large-scale enterprise networks, reducing the associated costs and required 
resources whilst improving security and efficiency.

It supports your engineering and operations teams, underpinning migration and 
transformation projects. IP Fabric will revolutionize how you approach network 
visibility and assurance, security assurance, automation, multi-cloud 
networking, and trouble resolution.

**Integrations or scripts should not be installed directly on the IP Fabric VM unless directly communicated from the
IP Fabric Support or Solution Architect teams.  Any action on the Command-Line Interface (CLI) using the root, osadmin,
or autoboss account may cause irreversible, detrimental changes to the product and can render the system unusable.**

## Project Description

**This is still in Beta release testing.**

This project is a CLI tool to synchronize network data discovered from IP Fabric into Infoblox.

Supported Models:
  - Networks

## Installation

```pip
pip install ipfabric-infoblox
```

## Configuration

1. Ensure you have a configuration file in `config.yml`:
```yaml
---
networkViews:
  - name: default
    default: true
    managed_ip_discovery: true
    # create_containerless_nets: true
    # split_networks: false
ipfabric:
  vrf_mapping:
    '':
      names:
        - default
        - main
        - ''
```

2. Ensure credentials are set in the environment:

```bash
IPF_TOKEN=
IPF_URL=https://<url>/

IB_USERNAME=
IB_PASSWORD=
IB_HOST=
IB_VERIFY_SSL=false
```

## Usage

1. Run a diff against the current state of the network:

```bash
ipfabric-infoblox diff
```

2. Apply the changes to the Infoblox:

```bash
ipfabric-infoblox sync
```

## Support

Please open a Gitlab Issue for support.
