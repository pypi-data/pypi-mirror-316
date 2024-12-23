import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
import time
from datetime import datetime
import socket
import subprocess

console = Console()

def format_bytes(bytes_value):
    """Format bytes into human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"

def get_connection_type(type_id):
    """Convert connection type ID to readable string."""
    return {
        socket.SOCK_STREAM: 'TCP',
        socket.SOCK_DGRAM: 'UDP',
        socket.SOCK_RAW: 'RAW'
    }.get(type_id, 'UNKNOWN')

def get_connection_status(status):
    """Convert connection status to readable string."""
    return {
        psutil.CONN_ESTABLISHED: 'ESTABLISHED',
        psutil.CONN_SYN_SENT: 'SYN_SENT',
        psutil.CONN_SYN_RECV: 'SYN_RECV',
        psutil.CONN_FIN_WAIT1: 'FIN_WAIT1',
        psutil.CONN_FIN_WAIT2: 'FIN_WAIT2',
        psutil.CONN_TIME_WAIT: 'TIME_WAIT',
        psutil.CONN_CLOSE: 'CLOSE',
        psutil.CONN_CLOSE_WAIT: 'CLOSE_WAIT',
        psutil.CONN_LAST_ACK: 'LAST_ACK',
        psutil.CONN_LISTEN: 'LISTENING',
        psutil.CONN_CLOSING: 'CLOSING',
        psutil.CONN_NONE: 'NONE'
    }.get(status, 'UNKNOWN')

def display_network_io():
    """Display network interface statistics."""
    interfaces = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    
    table = Table(
        title="Network Interface Statistics",
        show_header=True,
        header_style="bold magenta",
        title_style="bold blue"
    )
    
    table.add_column("Interface", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Speed", justify="right")
    table.add_column("MTU", justify="right", style="dim")
    table.add_column("Bytes Sent", justify="right", style="yellow")
    table.add_column("Bytes Received", justify="right", style="green")
    table.add_column("Packets Sent", justify="right", style="dim")
    table.add_column("Packets Received", justify="right", style="dim")
    
    for interface, stats in interfaces.items():
        if interface in io_counters:
            io = io_counters[interface]
            status = "🟢 Up" if stats.isup else "🔴 Down"
            speed = f"{stats.speed} Mb/s" if stats.speed > 0 else "N/A"
            
            table.add_row(
                interface,
                status,
                speed,
                str(stats.mtu),
                format_bytes(io.bytes_sent),
                format_bytes(io.bytes_recv),
                str(io.packets_sent),
                str(io.packets_recv)
            )
    
    console.print("\n")
    console.print(Panel(table, title="Network Interfaces", border_style="blue"))

def display_network_connections():
    """List all active network connections."""
    try:
        connections = psutil.net_connections(kind='all')
        
        table = Table(
            title="Active Network Connections",
            show_header=True,
            header_style="bold magenta",
            title_style="bold blue"
        )
        
        table.add_column("Protocol", style="cyan")
        table.add_column("Local Address", style="green")
        table.add_column("Remote Address", style="yellow")
        table.add_column("Status", style="magenta")
        table.add_column("PID", justify="right", style="dim")
        table.add_column("Process", style="bright_blue")
        
        for conn in connections:
            try:
                process = psutil.Process(conn.pid) if conn.pid else None
                local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                
                table.add_row(
                    get_connection_type(conn.type),
                    local_addr,
                    remote_addr,
                    get_connection_status(conn.status),
                    str(conn.pid or ""),
                    process.name() if process else ""
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        console.print("\n")
        console.print(Panel(table, title="Network Connections", border_style="blue"))
        
        # Add connection summary
        summary = Table.grid()
        summary.add_column(style="dim")
        status_count = {}
        for conn in connections:
            status = get_connection_status(conn.status)
            status_count[status] = status_count.get(status, 0) + 1
        
        summary.add_row("\nConnection Summary:")
        for status, count in status_count.items():
            summary.add_row(f"  • {status}: {count} connection(s)")
        
        console.print(summary)
        
    except psutil.AccessDenied:
        # Alternative implementation using netstat for macOS/Unix
        console.print("\n[yellow]Note: Root privileges required for detailed connection information.[/yellow]")
        console.print("[yellow]Using alternative method to show network connections...[/yellow]\n")
        
        table = Table(
            title="Network Connections (Limited Information)",
            show_header=True,
            header_style="bold magenta",
            title_style="bold blue"
        )
        
        table.add_column("Protocol", style="cyan")
        table.add_column("Local Address", style="green")
        table.add_column("Remote Address", style="yellow")
        table.add_column("State", style="magenta")
        
        try:
            # Use netstat to get connection information (available without root)
            cmd = "netstat -an"
            output = subprocess.check_output(cmd, shell=True, text=True)
            
            # Track connection states for summary
            state_count = {}
            
            for line in output.splitlines():
                # Skip header lines
                if not line or line.startswith("Proto") or line.startswith("Active"):
                    continue
                    
                parts = line.split()
                if len(parts) >= 5:
                    proto = parts[0]
                    local = parts[3]
                    remote = parts[4]
                    state = parts[5] if len(parts) > 5 else "ESTABLISHED"
                    
                    # Skip Unix domain sockets
                    if proto.startswith("unix"):
                        continue
                        
                    # Update state count
                    state_count[state] = state_count.get(state, 0) + 1
                    
                    table.add_row(
                        proto,
                        local,
                        remote,
                        state
                    )
            
            console.print(Panel(table, border_style="blue"))
            
            # Add connection summary
            if state_count:
                summary = Table.grid()
                summary.add_column(style="dim")
                summary.add_row("\nConnection Summary:")
                for state, count in state_count.items():
                    summary.add_row(f"  • {state}: {count} connection(s)")
                console.print(summary)
            else:
                console.print("[yellow]No active network connections found.[/yellow]")
            
            console.print("\n[dim]Note: For full connection information including processes, run with sudo:[/dim]")
            console.print("[dim]sudo python src/main.py network-connections[/dim]")
            
        except subprocess.CalledProcessError:
            console.print("[red]Error: Unable to retrieve network connections using alternative method.[/red]")
            console.print("\n[dim]To see complete connection information, run with sudo:[/dim]")
            console.print("[dim]sudo python src/main.py network-connections[/dim]")

def display_network_speed():
    """Monitor real-time network speed."""
    console.print("\n[bold blue]Network Speed Monitor[/bold blue] (Press Ctrl+C to stop)")
    
    try:
        # Initial stats
        prev_io = psutil.net_io_counters(pernic=True)
        time.sleep(1)  # Wait for initial data
        
        while True:
            current_io = psutil.net_io_counters(pernic=True)
            
            table = Table(show_header=True, header_style="bold magenta", title_style="bold blue")
            table.add_column("Interface", style="cyan")
            table.add_column("Download Speed", justify="right", style="green")
            table.add_column("Upload Speed", justify="right", style="yellow")
            table.add_column("Total Downloaded", justify="right", style="dim")
            table.add_column("Total Uploaded", justify="right", style="dim")
            
            for interface, stats in current_io.items():
                prev_stats = prev_io[interface]
                
                # Calculate speeds
                download_speed = stats.bytes_recv - prev_stats.bytes_recv
                upload_speed = stats.bytes_sent - prev_stats.bytes_sent
                
                table.add_row(
                    interface,
                    f"{format_bytes(download_speed)}/s",
                    f"{format_bytes(upload_speed)}/s",
                    format_bytes(stats.bytes_recv),
                    format_bytes(stats.bytes_sent)
                )
            
            # Clear screen and update display
            console.clear()
            console.print(f"\n[bold blue]Network Speed Monitor[/bold blue] (Press Ctrl+C to stop)")
            console.print(f"[dim]Last updated: {datetime.now().strftime('%H:%M:%S')}[/dim]")
            console.print(Panel(table, border_style="blue"))
            
            prev_io = current_io
            time.sleep(1)
            
    except KeyboardInterrupt:
        console.print("\n[dim]Stopped monitoring network speed[/dim]")

def display_open_ports():
    """Show all open ports and associated processes."""
    try:
        connections = psutil.net_connections(kind='all')
        
        table = Table(
            title="Open Ports",
            show_header=True,
            header_style="bold magenta",
            title_style="bold blue"
        )
        
        table.add_column("Protocol", style="cyan")
        table.add_column("Port", justify="right", style="yellow")
        table.add_column("State", style="green")
        table.add_column("PID", justify="right", style="dim")
        table.add_column("Process", style="bright_blue")
        table.add_column("Local Address", style="dim")
        
        # Sort connections by port number for better readability
        sorted_connections = sorted(
            [conn for conn in connections if conn.laddr],
            key=lambda x: (x.laddr.port if x.laddr else 0)
        )
        
        for conn in sorted_connections:
            try:
                if conn.laddr:  # Only show connections with local address
                    process = psutil.Process(conn.pid) if conn.pid else None
                    local_addr = f"{conn.laddr.ip}" if conn.laddr else "N/A"
                    
                    table.add_row(
                        get_connection_type(conn.type),
                        str(conn.laddr.port),
                        get_connection_status(conn.status),
                        str(conn.pid or ""),
                        process.name() if process else "",
                        local_addr
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        console.print("\n")
        console.print(Panel(table, title="Open Ports and Processes", border_style="blue"))
        
        # Add port summary
        summary = Table.grid()
        summary.add_column(style="dim")
        protocol_count = {}
        listening_ports = sum(1 for conn in sorted_connections if conn.status == psutil.CONN_LISTEN)
        
        for conn in sorted_connections:
            proto = get_connection_type(conn.type)
            protocol_count[proto] = protocol_count.get(proto, 0) + 1
        
        summary.add_row("\nPort Summary:")
        summary.add_row(f"  • Total Open Ports: {len(sorted_connections)}")
        summary.add_row(f"  • Listening Ports: {listening_ports}")
        for proto, count in protocol_count.items():
            summary.add_row(f"  • {proto}: {count} port(s)")
        
        console.print(summary)
        
    except psutil.AccessDenied:
        # Alternative implementation using netstat for macOS/Unix
        console.print("\n[yellow]Note: Root privileges required for detailed port information.[/yellow]")
        console.print("[yellow]Using alternative method to show listening ports...[/yellow]\n")
        
        table = Table(
            title="Listening Ports (Limited Information)",
            show_header=True,
            header_style="bold magenta",
            title_style="bold blue"
        )
        
        table.add_column("Protocol", style="cyan")
        table.add_column("Port", justify="right", style="yellow")
        table.add_column("Local Address", style="dim")
        
        try:
            # Use netstat to get listening ports (available on most systems without root)
            cmd = "netstat -an | grep LISTEN"
            output = subprocess.check_output(cmd, shell=True, text=True)
            
            # Parse netstat output
            seen_ports = set()
            for line in output.splitlines():
                parts = line.split()
                if len(parts) >= 4:
                    local_addr = parts[3]
                    if "." in local_addr:
                        # IPv4
                        addr, port = local_addr.rsplit(".", 1)
                        proto = "TCP"
                    elif ":" in local_addr:
                        # IPv6
                        addr, port = local_addr.rsplit(":", 1)
                        proto = "TCP6"
                    else:
                        continue
                    
                    if port not in seen_ports:
                        seen_ports.add(port)
                        table.add_row(proto, port, addr)
            
            if len(seen_ports) > 0:
                console.print(Panel(table, border_style="blue"))
                
                # Add summary
                summary = Table.grid()
                summary.add_column(style="dim")
                summary.add_row("\nPort Summary:")
                summary.add_row(f"  • Total Listening Ports: {len(seen_ports)}")
                console.print(summary)
            else:
                console.print("[yellow]No listening ports found.[/yellow]")
            
            console.print("\n[dim]Note: For full port information including processes, run with sudo:[/dim]")
            console.print("[dim]sudo python src/main.py ports[/dim]")
            
        except subprocess.CalledProcessError:
            console.print("[red]Error: Unable to retrieve port information using alternative method.[/red]")
            console.print("\n[dim]To see complete port information, run with sudo:[/dim]")
            console.print("[dim]sudo python src/main.py ports[/dim]")
  