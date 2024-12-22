import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.text import Text
from rich.style import Style
from rich.box import DOUBLE, ROUNDED
from rich.tree import Tree
from rich import print as rprint
import sys
import pyperclip
import string
import random
from password_strength import PasswordPolicy
import json
from pathlib import Path
from .password_store import PasswordStore

console = Console()

# Create a styled header
def print_header():
    header = Panel(
        Text("Pass-Master", style="bold cyan", justify="center"),
        subtitle="Secure Password Manager",
        box=DOUBLE,
        style="cyan",
        padding=(1, 2)
    )
    console.print(header)
    console.print()

# Password policy with rich display
policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    numbers=1,
    special=1,
)

def generate_password(length: int = 16) -> str:
    """Generate a secure random password"""
    with console.status("[bold cyan]Generating secure password...", spinner="dots"):
        characters = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(random.choice(characters) for _ in range(length))
            if policy.test(password) == []:
                return password

def check_password_strength(password: str) -> tuple[bool, str]:
    """Check password strength and return (is_strong, message)"""
    results = policy.test(password)
    if not results:
        return True, Panel("[green]Strong password![/green]", style="green", box=ROUNDED)
    
    tree = Tree(":warning: [yellow]Password is weak:[/yellow]")
    for result in results:
        if result.__class__.__name__ == 'Length':
            tree.add(":x: Must be at least 8 characters long")
        elif result.__class__.__name__ == 'Uppercase':
            tree.add(":x: Must contain at least 1 uppercase letter")
        elif result.__class__.__name__ == 'Numbers':
            tree.add(":x: Must contain at least 1 number")
        elif result.__class__.__name__ == 'Special':
            tree.add(":x: Must contain at least 1 special character")
    
    return False, tree

store = PasswordStore()

@click.group()
def cli() -> None:
    """Secure Password Manager"""
    print_header()

@cli.command()
@click.argument('service')
@click.option('--username', '-u', prompt=True, help='Username for the service')
@click.option('--password', '-p', prompt=True, hide_input=True, confirmation_prompt=True, 
              help='Password for the service')
@click.option('--generate/--no-generate', '-g', default=False, help='Generate a secure password')
@click.option('--length', '-l', default=16, help='Length of generated password')
@click.option('--category', '-c', help='Category for the password entry')
def add(service: str, username: str, password: str, generate: bool, length: int, category: str):
    """Add or update a password entry"""
    try:
        if generate:
            password = generate_password(length)
            console.print(Panel(f"Generated password: {password}", 
                              title="[cyan]Generated Password[/cyan]",
                              style="cyan"))
            pyperclip.copy(password)
            console.print("[green]✓[/green] Password copied to clipboard!")
        
        is_strong, message = check_password_strength(password)
        console.print(message)
        
        if not is_strong and not Confirm.ask("[yellow]Continue with weak password?[/yellow]"):
            return

        with console.status("[cyan]Saving password...", spinner="dots"):
            store.add_password(service, username, password, category)
        
        console.print(Panel(
            f"[green]✓[/green] Password saved for [cyan]{service}[/cyan]",
            style="green",
            box=ROUNDED
        ))
    except Exception as e:
        console.print(Panel(
            f"[red]Error saving password: {str(e)}[/red]",
            style="red",
            box=ROUNDED
        ))

@cli.command()
@click.argument('service')
@click.option('--copy/--no-copy', '-c', default=False, help='Copy password to clipboard')
def get(service: str, copy: bool):
    """Retrieve a password entry"""
    with console.status("[cyan]Retrieving password...", spinner="dots"):
        result = store.get_password(service)
    
    if result:
        username, password, category = result
        table = Table(show_header=True, box=ROUNDED)
        table.add_column("Service", style="cyan", header_style="bold cyan")
        table.add_column("Username", style="green", header_style="bold green")
        table.add_column("Password", style="magenta", header_style="bold magenta")
        table.add_column("Category", style="yellow", header_style="bold yellow")
        table.add_row(service, username, password, category or "")
        
        console.print(Panel(table, title="Password Details", border_style="cyan"))
        
        if copy:
            pyperclip.copy(password)
            console.print("[green]✓[/green] Password copied to clipboard!")
    else:
        console.print(Panel(
            f"[yellow]No password found for {service}[/yellow]",
            style="yellow",
            box=ROUNDED
        ))

@cli.command()
@click.option('--category', '-c', help='Filter by category')
def list(category: str):
    """List all stored services"""
    with console.status("[cyan]Loading passwords...", spinner="dots"):
        services = store.list_services(category)
    
    if services:
        table = Table(show_header=True, box=ROUNDED, title="Stored Passwords")
        table.add_column("Service", style="cyan", header_style="bold cyan")
        table.add_column("Username", style="green", header_style="bold green")
        table.add_column("Category", style="yellow", header_style="bold yellow")
        
        for service, username, cat in services:
            table.add_row(service, username, cat or "")
        console.print(table)
    else:
        console.print(Panel(
            "[yellow]No passwords stored yet[/yellow]",
            style="yellow",
            box=ROUNDED
        ))

@cli.command()
@click.argument('query')
def search(query: str):
    """Search for password entries"""
    with console.status(f"[cyan]Searching for '{query}'...", spinner="dots"):
        results = store.search_services(query)
    
    if results:
        table = Table(show_header=True, box=ROUNDED, title=f"Search Results for '{query}'")
        table.add_column("Service", style="cyan", header_style="bold cyan")
        table.add_column("Username", style="green", header_style="bold green")
        table.add_column("Category", style="yellow", header_style="bold yellow")
        
        for service, username, category in results:
            table.add_row(service, username, category or "")
        console.print(table)
    else:
        console.print(Panel(
            f"[yellow]No services found matching '{query}'[/yellow]",
            style="yellow",
            box=ROUNDED
        ))

@cli.command()
@click.option('--length', '-l', default=16, help='Password length')
def generate(length: int):
    """Generate a secure random password"""
    password = generate_password(length)
    console.print(Panel(
        f"Generated password: {password}",
        title="[cyan]Generated Password[/cyan]",
        style="cyan",
        box=ROUNDED
    ))
    pyperclip.copy(password)
    console.print("[green]✓[/green] Password copied to clipboard!")

@cli.command()
@click.argument('file', type=click.Path())
def export(file):
    """Export passwords to a JSON file"""
    try:
        with console.status("[cyan]Exporting passwords...", spinner="dots"):
            data = store.export_data()
            Path(file).write_text(json.dumps(data, indent=2))
        
        console.print(Panel(
            f"[green]✓[/green] Passwords exported to {file}",
            style="green",
            box=ROUNDED
        ))
    except Exception as e:
        console.print(Panel(
            f"[red]Error exporting passwords: {str(e)}[/red]",
            style="red",
            box=ROUNDED
        ))

@cli.command()
@click.argument('file', type=click.Path(exists=True))
def import_file(file):
    """Import passwords from a JSON file"""
    try:
        data = json.loads(Path(file).read_text())
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Importing passwords...", total=len(data))
            for service, entry in data.items():
                store.add_password(
                    service, 
                    entry['username'], 
                    entry['password'],
                    entry.get('category')
                )
                progress.advance(task)
        
        console.print(Panel(
            f"[green]✓[/green] Successfully imported {len(data)} passwords from {file}",
            style="green",
            box=ROUNDED
        ))
    except Exception as e:
        console.print(Panel(
            f"[red]Error importing passwords: {str(e)}[/red]",
            style="red",
            box=ROUNDED
        ))

if __name__ == '__main__':
    cli() 