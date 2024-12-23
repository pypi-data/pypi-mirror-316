import psutil
from rich.console import Console
from rich.progress import Progress
from src.utils.converter import bytes_to_human_readable

console = Console()

def get_memory_usage():
    """Fetch the current memory usage details."""
    memory = psutil.virtual_memory()
    used = bytes_to_human_readable(memory.used)
    total = bytes_to_human_readable(memory.total)
    return memory.percent, used, total

def display_memory_usage():
    """Display memory usage with a progress bar and detailed information."""
    usage, used, total = get_memory_usage()
    with Progress() as progress:
        task = progress.add_task("[cyan]Memory Usage", total=100)
        progress.update(task, completed=usage)
        console.print(f"Memory Usage: {used} / {total} ({usage}%)", style="bold green")
