import os
import sys
import tty
import termios
import subprocess
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt

console = Console()
ntfy_topic = None

def print_banner():
   banner = """
   ▄████████ ███    █▄  ▀█████████▄   ▄██████▄  ███    █▄  ████████▄   ▄█  
  ███    ███ ███    ███   ███    ███ ███    ███ ███    ███ ███   ▀███ ███  
  ███    █▀  ███    ███   ███    ███ ███    ███ ███    ███ ███    ███ ███▌ 
  ███        ███    ███  ▄███▄▄▄██▀  ███    ███ ███    ███ ███    ███ ███▌ 
▀███████████ ███    ███ ▀▀███▀▀▀██▄  ███    ███ ███    ███ ███    ███ ███▌ 
         ███ ███    ███   ███    ██▄ ███    ███ ███    ███ ███    ███ ███  
   ▄█    ███ ███    ███   ███    ███ ███    ███ ███    ███ ███   ▄███ ███  
 ▄████████▀  ████████▀  ▄█████████▀   ▀██████▀  ████████▀  ████████▀  █▀  
"""
   console.print(Panel(Align.center(banner), border_style="bold cyan"))
   console.print(Panel("[bold magenta]POWERED BY ABDELRAHMAN KHALED | LINKEDIN:https://www.linkedin.com/in/abdelrahmankhaledahmed | GITHUB: https://github.com/Boudi0x[/bold magenta]", border_style="magenta"), "\n")

def get_single_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def send_notification(message):
    global ntfy_topic
    if ntfy_topic:
        subprocess.call(f"curl -s -d \"{message}\" ntfy.sh/{ntfy_topic} > /dev/null 2>&1", shell=True)

def run_command_with_spinner(command, description, output_file):
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn(f"[bold cyan]{description.upper()}..."),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task(description.upper(), start=False)
        with open(output_file, "w") as out_f:
            process = subprocess.Popen(command, stdout=out_f, stderr=subprocess.DEVNULL, shell=True)
            progress.start_task(task)
            while process.poll() is None:
                time.sleep(0.1)
        process.wait()

    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            lines = set(line.strip() for line in f if line.strip())
        if len(lines) == 0:
            console.print(Panel(f"[red]NO RESULTS FOUND DURING {description.upper()}.[/red]", border_style="red"))
        return lines
    else:
        console.print(Panel(f"[red]{description.upper()} FAILED OR OUTPUT FILE MISSING.[/red]", border_style="red"))
        return set()

def read_file_set(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def choose_mode():
    console.print(Panel("[bold yellow]SELECT SCAN MODE[/bold yellow]\n\n"
                        "[green][ENTER][/green] - MANUAL MODE (ENTER TARGET DOMAINS MANUALLY)\n"
                        "[green][SPACE][/green] - RECON MODE (AUTOMATED SUBDOMAIN ENUMERATION)",
                        border_style="yellow"))
    key = get_single_key()
    if key in ("\r", "\n"):
        console.print(Panel("[bold green]MANUAL MODE SELECTED[/bold green]", border_style="green"))
        return "manual"
    elif key == " ":
        console.print(Panel("[bold green]RECON MODE SELECTED[/bold green]", border_style="green"))
        return "recon"
    else:
        console.print(Panel("[bold red]INVALID INPUT. DEFAULTING TO MANUAL MODE.[/bold red]", border_style="red"))
        return "manual"

def ask_ntfy_topic():
    global ntfy_topic
    ntfy_topic = Prompt.ask("[bold cyan]ENTER NTFY.SH TOPIC NAME TO RECEIVE NOTIFICATION OR PRESS ENTER TO SKIP[/bold cyan]").strip()
    if ntfy_topic:
        console.print(Panel(f"[green]NOTIFICATIONS WILL BE SENT TO: [cyan]{ntfy_topic}[/cyan][/green]", border_style="green"))
    else:
        ntfy_topic = None
        console.print(Panel("[yellow]NO NOTIFICATIONS WILL BE SENT.[/yellow]", border_style="yellow"))

def main():
    print_banner()
    ask_ntfy_topic()
    mode = choose_mode()

    if mode == "manual":
        file_name = Prompt.ask("[bold cyan] PLEASE ENTER THE NAME OF THE FOLDER ( WILL BE CREATED AT HOME )[/bold cyan]").strip()
        path = os.path.join(os.path.expanduser("~"), file_name)
        os.makedirs(path, exist_ok=True)

        console.print(Panel("[bold yellow]ENTER THE DOMAINS YOU WANT TO TEST MANUALLY. SUBMIT AN EMPTY LINE TO FINISH.[/bold yellow]", border_style="yellow"))
        domains = []
        while True:
            domain = Prompt.ask("[bold cyan]ENTER DOMAIN[/bold cyan]").strip()
            if not domain:
                break
            if not domain.startswith("http"):
                domain = "https://" + domain
            domains.append(domain)

        manual_file = os.path.join(path, "Manual_Testing.txt")
        with open(manual_file, 'w') as f:
            f.write("\n".join(domains))
        console.print(Panel(f"[bold green]MANUAL DOMAINS SAVED SUCCESSFULLY TO:\n{manual_file.upper()}[/bold green]", border_style="green"))

    else:
        website_name = Prompt.ask("[bold cyan] PLEASE ENTER THE NAME OF THE FOLDER ( WILL BE CREATED AT HOME )[/bold cyan]").strip()
        path = os.path.join(os.path.expanduser("~"), website_name)
        os.makedirs(path, exist_ok=True)

        console.print(Panel("[bold yellow]ENTER WILDCARD DOMAIN(S) FOR SUBDOMAIN ENUMERATION (E.G., EXAMPLE.COM). SUBMIT AN EMPTY LINE TO FINISH.[/bold yellow]", border_style="yellow"))
        domains = []
        while True:
            domain = Prompt.ask("[bold cyan]ENTER WILDCARD DOMAIN[/bold cyan]").strip()
            if not domain:
                break
            domains.append(domain)

        domains_file = os.path.join(path, "domains.txt")
        with open(domains_file, 'w') as f:
            f.write("\n".join(domains))

        subfinder_file = os.path.join(path, "subfinder.txt")
        subfinder_deep_file = os.path.join(path, "subfinder_deep.txt")
        assetfinder_file = os.path.join(path, "assetfinder.txt")
        crtsh_file = os.path.join(path, "crtsh.txt")

        # Subfinder
        subfinder_lines = run_command_with_spinner(
            f"subfinder -dL {domains_file} -all -silent -o {subfinder_file}",
            "Running Subfinder",
            subfinder_file
        )
        console.print(Panel(f"[bold green]SUBFINDER DISCOVERED [cyan]{len(subfinder_lines)}[/cyan] UNIQUE SUBDOMAINS.[/bold green]", border_style="green"))
        send_notification(f"Subfinder Finished. Found {len(subfinder_lines)} Subdomains.")

        # Deep Subfinder
        deep_lines = run_command_with_spinner(
            f"subfinder -dL {subfinder_file} -all -silent -o {subfinder_deep_file}",
            "Running Deep Subfinder",
            subfinder_deep_file
        )
        console.print(Panel(f"[bold green]DEEP SUBFINDER DISCOVERED [cyan]{len(deep_lines)}[/cyan] UNIQUE SUBDOMAINS.[/bold green]", border_style="green"))
        send_notification(f"Deep Subfinder Finished. Found {len(deep_lines)} Subdomains.")

        # Assetfinder
        assetfinder_lines = run_command_with_spinner(
            f"for d in {' '.join(domains)}; do assetfinder $d; done > {assetfinder_file}",
            "Running Assetfinder",
            assetfinder_file
        )
        console.print(Panel(f"[bold green]ASSETFINDER DISCOVERED [cyan]{len(assetfinder_lines)}[/cyan] UNIQUE SUBDOMAINS.[/bold green]", border_style="green"))
        send_notification(f"Assetfinder Finished. Found {len(assetfinder_lines)} Subdomains.")

        # crt.sh
        crtsh_lines = run_command_with_spinner(
            f"for d in {' '.join(domains)}; do /home/Tools/crt.sh/./crt_v2.sh -d $d; done > {crtsh_file}",
            "Running crt.sh",
            crtsh_file
        )
        console.print(Panel(f"[bold green]CRT.SH DISCOVERED [cyan]{len(crtsh_lines)}[/cyan] UNIQUE SUBDOMAINS.[/bold green]", border_style="green"))
        send_notification(f"Crt.sh Finished. Found {len(crtsh_lines)} Subdomains.")


        # Combine all unique subdomains
        combined_domains = sorted(subfinder_lines | deep_lines | assetfinder_lines | crtsh_lines)
        combined_file = os.path.join(path, "combined.txt")
        with open(combined_file, 'w') as f:
            f.write("\n".join(combined_domains))
        console.print(Panel(f"[bold green]TOTAL UNIQUE SUBDOMAINS AFTER COMBINATION: [cyan]{len(combined_domains)}[/cyan][/bold green]", border_style="green"))
        send_notification(f"All Tools Combined. Total Unique Subdomains: {len(combined_domains)}.")

        # httpx 2xx
        httpx_2xx_out = os.path.join(path, "Subdomains_2xx.txt")
        httpx_2xx_lines = run_command_with_spinner(
            f"httpx -l {combined_file} -o {httpx_2xx_out} -rl 100 -retries 2 -mc 200",
            "Running httpx to identify live subdomains with 2xx status",
            httpx_2xx_out
        )
        console.print(Panel(f"[bold green]HTTPX FOUND [cyan]{len(httpx_2xx_lines)}[/cyan] SUBDOMAINS RESPONDING WITH 2XX STATUS CODES.[/bold green]", border_style="green"))
        send_notification(f"Httpx (2xx) Finished. Found {len(httpx_2xx_lines)} Live Subdomains.")


        # httpx 3xx
        httpx_3xx_out = os.path.join(path, "Subdomains_3xx.txt")
        httpx_3xx_lines = run_command_with_spinner(
            f"httpx -l {combined_file} -o {httpx_3xx_out} -rl 100 -retries 2 -mc 301,302",
            "Running httpx to identify subdomains with 3xx status",
            httpx_3xx_out
        )
        console.print(Panel(f"[bold green]HTTPX FOUND [cyan]{len(httpx_3xx_lines)}[/cyan] SUBDOMAINS RESPONDING WITH 3XX STATUS CODES.[/bold green]", border_style="green"))
        send_notification(f"Httpx (3xx) Finished. Found {len(httpx_3xx_lines)} Subdomains.")


        # httpx 4xx
        httpx_4xx_out = os.path.join(path, "Subdomains_4xx.txt")
        httpx_4xx_lines = run_command_with_spinner(
            f"httpx -l {combined_file} -o {httpx_4xx_out} -rl 100 -retries 2 -mc 403,404",
            "Running httpx to identify subdomains with 4xx status",
            httpx_4xx_out
        )
        console.print(Panel(f"[bold green]HTTPX FOUND [cyan]{len(httpx_4xx_lines)}[/cyan] SUBDOMAINS RESPONDING WITH 4XX STATUS CODES.[/bold green]", border_style="green"))
        send_notification(f"Httpx (4xx) Finished. Found {len(httpx_4xx_lines)} Subdomains.")


        # Delete all other txt files except 2xx / 3xx / 4xx
        for file in os.listdir(path):
            if file.endswith(".txt") and file not in ["Subdomains_2xx.txt", "Subdomains_3xx.txt", "Subdomains_4xx.txt"]:
                os.remove(os.path.join(path, file))

    console.print(Panel("[bold blue]✔ SCAN COMPLETED SUCCESSFULLY![/bold blue]", border_style="blue", padding=(1, 4)))
    console.print()
    send_notification("Subdomains Enumeration Scan Completed.")

if __name__ == "__main__":
    main()
