import typer
from rich.console import Console
from rich.panel import Panel
import pyfiglet
from typing import Optional
from src.metrics.cpu import display_cpu_usage, display_cpu_info
from src.metrics.memory import display_memory_usage
from src.metrics.disk import display_disk_usage, display_disk_io, display_disk_partitions
from src.metrics.network import display_network_io, display_network_connections, display_network_speed, display_open_ports
from src.metrics.system import display_system_info, display_boot_time, display_battery

app = typer.Typer(
    help="A comprehensive system monitoring CLI tool",
    rich_markup_mode="rich",
    add_completion=False,
    no_args_is_help=False
)
console = Console()

def display_banner():
    """Display the styled banner for syswatcher"""
    banner = pyfiglet.figlet_format("SysWatcher", font="slant")
    console.print(f"\n[cyan]{banner}[/cyan]")
    console.print("[yellow]A comprehensive system monitoring tool[/yellow]\n")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, help: bool = typer.Option(False, "--help", "-h", is_eager=True)):
    """
    SysWatcher - A comprehensive system monitoring CLI tool
    """
    if help or ctx.invoked_subcommand is None:
        display_banner()
        if help:
            console.print(ctx.get_help())
        else:
            console.print("[bold cyan]Available commands:[/bold cyan]")
            console.print("\nRun [green]syswatcher COMMAND --help[/green] for detailed information about a command.\n")
        if help:
            raise typer.Exit()

@app.command("cpu")
def cpu():
    """Display real-time CPU usage metrics:
    - Overall CPU utilization
    - Per-core activity with visual indicators
    - CPU time distribution across states
    - Active cores summary and load averages
    """
    display_cpu_usage()

@app.command("cpu-info")
def cpu_info():
    """Display comprehensive CPU information including:
    - Basic CPU details (processor, architecture, cores)
    - Frequency information (current, min, max)
    - CPU statistics (context switches, interrupts)
    - CPU times (user, system, idle)
    - System load averages
    """
    display_cpu_info()

@app.command("memory")
def memory():
    """Monitor memory usage."""
    display_memory_usage()

@app.command("disk-usage")
def disk_usage():
    """Show disk space usage for all mounted partitions.
    Displays total, used, and free space with visual usage indicators."""
    display_disk_usage()

@app.command("disk-io")
def disk_io():
    """Display real-time disk I/O statistics.
    Shows read/write speeds and operation counts for all disks.
    Press Ctrl+C to stop monitoring."""
    display_disk_io()

@app.command("disk-partitions")
def disk_partitions():
    """List all disk partitions and their details.
    Shows mount points, file systems, and partition options."""
    display_disk_partitions()

@app.command("network-io")
def network_io():
    """Show network interface statistics:
    - Interface status and speed
    - Bytes sent/received
    - Packet counts
    - MTU and other details
    """
    display_network_io()

@app.command("network-connections")
def network_connections():
    """List all active network connections:
    - Protocol and status
    - Local and remote addresses
    - Associated processes
    - Connection states summary
    """
    display_network_connections()

@app.command("network-speed")
def network_speed():
    """Monitor real-time network speed:
    - Download and upload speeds
    - Per-interface monitoring
    - Total data transferred
    Press Ctrl+C to stop monitoring.
    """
    display_network_speed()

@app.command("ports")
def ports():
    """Show all open ports and associated processes:
    - Protocol and port number
    - Connection state
    - Process using the port
    - Listening ports summary
    """
    display_open_ports()

@app.command("system-info")
def system_info():
    """Show detailed system information:
    - OS details and version
    - CPU specifications
    - Memory information
    - System architecture
    - Host details
    """
    display_system_info()

@app.command("boot-time")
def boot_time():
    """Display system boot time and uptime:
    - System start time
    - Current uptime
    - Detailed time breakdown
    """
    display_boot_time()

@app.command("battery")
def battery():
    """Show battery status and details:
    - Battery percentage
    - Power source status
    - Time remaining
    - Charging status
    For laptops and portable devices.
    """
    display_battery()

if __name__ == "__main__":
    app()
    