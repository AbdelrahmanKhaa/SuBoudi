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
- `curl` installed (for notifications)
- Linux/macOS terminal (for running `crt_v2.sh` script)

## How to install Python dependencies

```bash
pip install rich
```
## Setup and Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/SuBoudi.git
cd SuBoudi
chmod +x crt_v2.sh

