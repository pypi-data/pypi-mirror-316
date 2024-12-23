import psutil
import platform
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import time

console = Console()

def get_size(bytes_value):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"

def display_system_info():
    """Show detailed system information."""
    # Get system information
    uname = platform.uname()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    
    # Create main system info table
    sys_table = Table(
        title="System Information",
        show_header=True,
        header_style="bold magenta",
        title_style="bold blue"
    )
    
    sys_table.add_column("Property", style="cyan")
    sys_table.add_column("Value", style="green")
    
    sys_table.add_row("OS", f"{uname.system}")
    sys_table.add_row("OS Version", f"{uname.version}")
    sys_table.add_row("OS Release", f"{uname.release}")
    sys_table.add_row("Architecture", f"{uname.machine}")
    sys_table.add_row("Processor", f"{uname.processor}")
    sys_table.add_row("Hostname", f"{uname.node}")
    sys_table.add_row("Boot Time", f"{boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # CPU Information
    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f}MHz" if hasattr(psutil.cpu_freq(), 'max') else "N/A",
        "Min Frequency": f"{psutil.cpu_freq().min:.2f}MHz" if hasattr(psutil.cpu_freq(), 'min') else "N/A"
    }
    
    # Memory Information
    memory = psutil.virtual_memory()
    memory_info = {
        "Total Memory": get_size(memory.total),
        "Available Memory": get_size(memory.available),
        "Memory Used": f"{memory.percent}%"
    }
    
    # Create CPU info table
    cpu_table = Table(title="CPU Information", show_header=True, header_style="bold magenta", title_style="bold blue")
    cpu_table.add_column("Property", style="cyan")
    cpu_table.add_column("Value", style="green")
    
    for key, value in cpu_info.items():
        cpu_table.add_row(key, str(value))
    
    # Create Memory info table
    mem_table = Table(title="Memory Information", show_header=True, header_style="bold magenta", title_style="bold blue")
    mem_table.add_column("Property", style="cyan")
    mem_table.add_column("Value", style="green")
    
    for key, value in memory_info.items():
        mem_table.add_row(key, str(value))
    
    # Display all tables with proper spacing
    console.print("\n")
    console.print(Panel(sys_table, title="System Overview", border_style="blue"))
    console.print("\n")
    console.print(Panel(cpu_table, title="CPU Details", border_style="green"))
    console.print("\n")
    console.print(Panel(mem_table, title="Memory Details", border_style="yellow"))

def display_boot_time():
    """Display system boot time and uptime."""
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp)
    current_time = datetime.now()
    
    uptime = current_time - boot_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    table = Table(
        title="System Uptime Information",
        show_header=True,
        header_style="bold magenta",
        title_style="bold blue"
    )
    
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Boot Time", boot_time.strftime('%Y-%m-%d %H:%M:%S'))
    table.add_row("Current Time", current_time.strftime('%Y-%m-%d %H:%M:%S'))
    table.add_row("Uptime", f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
    
    console.print("\n")
    console.print(Panel(table, title="System Uptime", border_style="blue"))

def display_battery():
    """Show battery status and details."""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            console.print("\n[yellow]No battery detected. This might be a desktop computer.[/yellow]")
            return
        
        table = Table(
            title="Battery Information",
            show_header=True,
            header_style="bold magenta",
            title_style="bold blue"
        )
        
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        # Calculate time left
        if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            hours, remainder = divmod(battery.secsleft, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            time_left = "Unlimited"
        
        # Battery percentage with color coding
        percentage = battery.percent
        if percentage >= 80:
            percent_color = "green"
        elif percentage >= 40:
            percent_color = "yellow"
        else:
            percent_color = "red"
        
        table.add_row(
            "Battery Percentage",
            f"[{percent_color}]{percentage}%[/{percent_color}]"
        )
        table.add_row(
            "Power Status",
            "🔌 Plugged In" if battery.power_plugged else "🔋 On Battery"
        )
        table.add_row("Time Left", time_left if not battery.power_plugged else "N/A (Charging)")
        
        # Create a battery level visualization
        bar_length = 40
        filled_length = int(percentage * bar_length / 100)
        bar = f"[{percent_color}]{'█' * filled_length}[/{percent_color}][dim]{'░' * (bar_length - filled_length)}[/dim]"
        
        console.print("\n")
        console.print(Panel(table, title="Battery Status", border_style="blue"))
        console.print(f"\nBattery Level: {bar}")
        
        if battery.power_plugged:
            console.print("\n[green]ℹ Power adapter is connected[/green]")
        elif percentage < 20:
            console.print("\n[red]⚠ Battery level is low![/red]")
        
    except Exception as e:
        console.print(f"\n[red]Error accessing battery information: {str(e)}[/red]")
        console.print("[yellow]This might be due to missing hardware or system limitations.[/yellow]") 