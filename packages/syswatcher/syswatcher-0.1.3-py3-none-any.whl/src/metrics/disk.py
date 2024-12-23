import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
import time

console = Console()

def get_disk_partitions():
    """Get information about disk partitions."""
    return psutil.disk_partitions(all=False)

def get_disk_usage(path):
    """Get disk usage statistics for a given path."""
    try:
        return psutil.disk_usage(path)
    except (PermissionError, FileNotFoundError):
        return None

def get_disk_io():
    """Get disk I/O statistics."""
    return psutil.disk_io_counters(perdisk=True)

def format_bytes(bytes_value):
    """Format bytes into human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"

def display_disk_usage():
    """Display disk space usage for all mounted partitions."""
    partitions = get_disk_partitions()
    
    table = Table(
        title="Disk Space Usage",
        show_header=True,
        header_style="bold magenta",
        title_style="bold blue"
    )
    
    table.add_column("Mount Point", style="cyan")
    table.add_column("Device", style="dim")
    table.add_column("Total", justify="right", style="green")
    table.add_column("Used", justify="right", style="yellow")
    table.add_column("Free", justify="right", style="green")
    table.add_column("Usage", justify="right")
    table.add_column("Type", style="dim")
    
    for partition in partitions:
        usage = get_disk_usage(partition.mountpoint)
        if usage:
            # Create usage bar
            usage_pct = usage.percent
            bar_length = 20
            filled_length = int(usage_pct * bar_length / 100)
            bar_color = "green" if usage_pct < 80 else "yellow" if usage_pct < 90 else "red"
            bar = f"[{bar_color}]{'█' * filled_length}[/][dim]{'░' * (bar_length - filled_length)}[/] {usage_pct:.1f}%"
            
            table.add_row(
                partition.mountpoint,
                partition.device,
                format_bytes(usage.total),
                format_bytes(usage.used),
                format_bytes(usage.free),
                bar,
                partition.fstype
            )
    
    console.print("\n")
    console.print(Panel(table, title="Disk Space Usage", border_style="blue"))
    console.print("\n[dim]Note: Usage bars are color-coded: green (<80%), yellow (80-90%), red (>90%)[/dim]")

def display_disk_io():
    """Display real-time disk I/O statistics."""
    console.print("\n[bold blue]Disk I/O Statistics[/bold blue] (Press Ctrl+C to stop)")
    
    try:
        # Initial I/O stats
        prev_io = get_disk_io()
        time.sleep(1)  # Wait for initial data
        
        while True:
            current_io = get_disk_io()
            
            table = Table(show_header=True, header_style="bold magenta", title_style="bold blue")
            table.add_column("Disk", style="cyan")
            table.add_column("Read Speed", justify="right", style="green")
            table.add_column("Write Speed", justify="right", style="yellow")
            table.add_column("Read Count", justify="right", style="dim")
            table.add_column("Write Count", justify="right", style="dim")
            
            for disk, stats in current_io.items():
                prev_stats = prev_io[disk]
                
                # Calculate rates
                read_bytes = stats.read_bytes - prev_stats.read_bytes
                write_bytes = stats.write_bytes - prev_stats.write_bytes
                read_count = stats.read_count - prev_stats.read_count
                write_count = stats.write_count - prev_stats.write_count
                
                table.add_row(
                    disk,
                    f"{format_bytes(read_bytes)}/s",
                    f"{format_bytes(write_bytes)}/s",
                    str(read_count),
                    str(write_count)
                )
            
            # Clear screen and update display
            console.clear()
            console.print("\n[bold blue]Real-time Disk I/O Statistics[/bold blue] (Press Ctrl+C to stop)")
            console.print(Panel(table, border_style="blue"))
            
            prev_io = current_io
            time.sleep(1)
            
    except KeyboardInterrupt:
        console.print("\n[dim]Stopped monitoring disk I/O[/dim]")

def display_disk_partitions():
    """Display detailed information about all disk partitions."""
    partitions = get_disk_partitions()
    
    table = Table(
        title="Disk Partitions",
        show_header=True,
        header_style="bold magenta",
        title_style="bold blue"
    )
    
    table.add_column("Device", style="cyan")
    table.add_column("Mount Point", style="green")
    table.add_column("File System", style="yellow")
    table.add_column("Options", style="dim")
    table.add_column("Max File Length", justify="right")
    table.add_column("Mount Flags", style="dim")
    
    for partition in partitions:
        # Get additional partition details
        maxfile = getattr(partition, 'maxfile', 'N/A')
        flags = getattr(partition, 'flags', 'N/A')
        
        table.add_row(
            partition.device,
            partition.mountpoint,
            partition.fstype,
            partition.opts,
            str(maxfile),
            str(flags)
        )
    
    console.print("\n")
    console.print(Panel(table, title="Disk Partitions Information", border_style="blue"))
    
    # Add partition type summary
    fs_types = {}
    for partition in partitions:
        fs_types[partition.fstype] = fs_types.get(partition.fstype, 0) + 1
    
    summary = Table.grid()
    summary.add_column(style="dim")
    summary.add_row(f"\nFile System Summary:")
    for fs_type, count in fs_types.items():
        summary.add_row(f"  • {fs_type}: {count} partition(s)")
    
    console.print(summary) 