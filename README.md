# SuBoudi - Automated Subdomain Enumerator with Notifications

This tool helps automate subdomain enumeration from multiple powerful sources and notifies you when the scan is complete.

## Features
- Aggregates subdomains from multiple sources.
- Sends a notification when the scan is finished.
- Fast and minimal Python-based tool.
- Includes the `crt_v2.sh` script for crt.sh enumeration.

## Requirements

- Python 3.x
- `subfinder`, `assetfinder`, `httpx` installed and available in PATH
- `curl` installed (for notification)
- Linux/macOS terminal (for `crt_v2.sh` script)
- Python package: [rich](https://pypi.org/project/rich/)

## How to install Python dependencies

```bash

1. Clone the repository:

```bash
git clone https://github.com/your-username/SuBoudi.git
cd SuBoudi
