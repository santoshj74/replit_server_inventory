#!/usr/bin/env python3
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from rich import box
import sys
import traceback
from data_manager import DataManager
from utils import clear_screen, validate_input

# Initialize rich console with defaults for better compatibility
console = Console(color_system="auto", force_terminal=True)

class ServerInventory:
    def __init__(self):
        rprint("[dim]ServerInventory.__init__ called[/dim]")
        self.data_manager = DataManager()
        self.commands = {
            'add': self.add_server,
            'list': self.list_servers,
            'search': self.search_servers,
            'delete': self.delete_server,
            'export': self.export_servers,
            'help': self.show_help,
            'exit': self.exit_program
        }

    def get_input(self, prompt, default=None):
        """Safely get user input with EOF handling."""
        try:
            return input(prompt).lower().strip()
        except EOFError:
            if default is not None:
                return default
            rprint("\n[yellow]Input terminated. Exiting...[/yellow]")
            self.exit_program()
        except KeyboardInterrupt:
            rprint("\n[yellow]Operation cancelled by user.[/yellow]")
            return ''

    def run(self):
        rprint("[dim]ServerInventory.run called[/dim]")
        clear_screen()
        self.show_welcome()

        while True:
            try:
                command = self.get_input("\nEnter command (type 'help' for commands): ")
                if not command:
                    continue

                rprint(f"[dim]Executing command: {command}[/dim]")
                if command in self.commands:
                    rprint(f"[dim]Calling command: {command}[/dim]")
                    self.commands[command]()
                else:
                    rprint("[red]Invalid command. Type 'help' for available commands.[/red]")
            except Exception as e:
                rprint(f"[red]An error occurred: {str(e)}[/red]")
                rprint(f"[dim]Debug traceback: {traceback.format_exc()}[/dim]")

    def show_welcome(self):
        rprint("[dim]ServerInventory.show_welcome called[/dim]")
        console.print("[blue]====================================")
        console.print("[green]Server Inventory Management System")
        console.print("[blue]====================================")

    def add_server(self):
        rprint("\n[yellow]Adding new server...[/yellow]")
        try:
            product_name = validate_input("Enter Product Name (e.g., Dell R740): ", str)
            serial_number = validate_input("Enter Serial Number (e.g., SN123456): ", str)
            rack_location = validate_input("Enter Rack Location (e.g., Rack-A1): ", str)
            username = validate_input("Enter Username (e.g., admin): ", str)

            server = {
                'product_name': product_name,
                'serial_number': serial_number,
                'rack_location': rack_location,
                'username': username
            }

            self.data_manager.add_server(server)
            rprint("[green]✓ Server added successfully![/green]")
        except (EOFError, KeyboardInterrupt):
            rprint("\n[yellow]Operation cancelled.[/yellow]")
        except ValueError as e:
            rprint(f"[red]Error: {str(e)}[/red]")
        except Exception as e:
            rprint(f"[red]An unexpected error occurred: {str(e)}[/red]")
            rprint(f"[dim]Debug traceback: {traceback.format_exc()}[/dim]")

    def list_servers(self):
        rprint("[dim]ServerInventory.list_servers called[/dim]")
        try:
            servers = self.data_manager.get_servers()
            if not servers:
                rprint("[yellow]No servers found in inventory.[/yellow]")
                return

            table = Table(title="Server Inventory")
            table.add_column("Product Name", style="cyan", no_wrap=True)
            table.add_column("Serial Number", style="magenta", no_wrap=True)
            table.add_column("Rack Location", style="green", no_wrap=True)
            table.add_column("Username", style="blue", no_wrap=True)

            for server in servers:
                table.add_row(
                    server['product_name'],
                    server['serial_number'],
                    server['rack_location'],
                    server['username']
                )

            console.print("\n")
            console.print(table)
        except Exception as e:
            rprint(f"[red]Error listing servers: {str(e)}[/red]")
            rprint(f"[dim]Debug traceback: {traceback.format_exc()}[/dim]")

    def search_servers(self):
        rprint("[dim]ServerInventory.search_servers called[/dim]")
        try:
            search_term = self.get_input("\nEnter search term: ")
            if not search_term:
                rprint("[yellow]Please enter a search term.[/yellow]")
                return

            servers = self.data_manager.search_servers(search_term)

            if not servers:
                rprint("[yellow]No matching servers found.[/yellow]")
                return

            table = Table(title=f"Search Results for '{search_term}'")
            table.add_column("Product Name", style="cyan", no_wrap=True)
            table.add_column("Serial Number", style="magenta", no_wrap=True)
            table.add_column("Rack Location", style="green", no_wrap=True)
            table.add_column("Username", style="blue", no_wrap=True)

            for server in servers:
                table.add_row(
                    server['product_name'],
                    server['serial_number'],
                    server['rack_location'],
                    server['username']
                )

            console.print("\n")
            console.print(table)
        except (EOFError, KeyboardInterrupt):
            rprint("\n[yellow]Search cancelled.[/yellow]")
        except Exception as e:
            rprint(f"[red]Error during search: {str(e)}[/red]")
            rprint(f"[dim]Debug traceback: {traceback.format_exc()}[/dim]")

    def delete_server(self):
        """Delete a server by its serial number."""
        rprint("\n[yellow]Deleting server...[/yellow]")
        try:
            serial_number = validate_input("Enter Serial Number to delete: ", str)
            if not serial_number:
                rprint("[yellow]Operation cancelled.[/yellow]")
                return

            self.data_manager.delete_server(serial_number)
            rprint("[green]✓ Server deleted successfully![/green]")
        except (EOFError, KeyboardInterrupt):
            rprint("\n[yellow]Delete operation cancelled.[/yellow]")
        except ValueError as e:
            rprint(f"[red]Error: {str(e)}[/red]")
        except Exception as e:
            rprint(f"[red]An unexpected error occurred: {str(e)}[/red]")
            rprint(f"[dim]Debug traceback: {traceback.format_exc()}[/dim]")

    def show_help(self):
        """Display the help menu with colorful command explanations."""
        try:
            rprint("[dim]Displaying help menu...[/dim]")

            # Create and display the main help panel with an interactive feel
            main_panel = Panel(
                "[bold cyan]📚 Server Inventory Help Guide[/bold cyan]\n" +
                "[white]Welcome to the interactive help system! Choose any command below to get started.[/white]",
                border_style="blue",
                padding=(1, 2)
            )
            console.print("\n", main_panel)

            # Create and display the commands table
            table = Table(
                title="🎯 Available Commands",
                show_header=True,
                header_style="bold magenta",
                box=box.ROUNDED,
                padding=(0, 2),
                min_width=60,
                title_style="bold cyan"
            )

            table.add_column("🔑 Command", style="cyan", width=12)
            table.add_column("📝 Description", style="green", width=30)
            table.add_column("💡 Example Usage", style="yellow", width=25)

            commands = [
                ("add", "Add a new server to inventory", "> add\n[dim]Then follow the prompts[/dim]"),
                ("list", "Display all servers in inventory", "> list\n[dim]Shows all servers[/dim]"),
                ("search", "Search servers by any field", "> search\n[dim]Enter term: dell[/dim]"),
                ("delete", "Delete server by serial number", "> delete\n[dim]Enter serial number[/dim]"),
                ("export", "Export inventory to CSV", "> export\n[dim]Creates .csv file[/dim]"),
                ("help", "Show this interactive guide", "> help"),
                ("exit", "Exit the program safely", "> exit")
            ]

            for cmd, desc, example in commands:
                table.add_row(
                    f"[bold cyan]{cmd}[/bold cyan]",
                    f"[green]{desc}[/green]",
                    f"[yellow]{example}[/yellow]"
                )

            console.print(table)

            # Create and display the tips panel with more engaging content
            tips_panel = Panel(
                "[bold yellow]💫 Pro Tips:[/bold yellow]\n" +
                "• Use [cyan]↑/↓ arrows[/cyan] to recall previous commands\n" +
                "• Press [cyan]Ctrl+C[/cyan] to exit safely at any time\n" +
                "• Commands are [cyan]case-insensitive[/cyan] for convenience\n" +
                "• Type a command and press [cyan]Enter[/cyan] to execute",
                title="🌟 Quick Tips",
                border_style="yellow",
                padding=(1, 2)
            )
            console.print("\n", tips_panel)

            console.print("\n[dim]✨ Type a command to begin...[/dim]")

        except Exception as e:
            rprint(f"[red]Error in help menu: {str(e)}[/red]")
            rprint(f"[dim]Debug traceback: {traceback.format_exc()}[/dim]")

    def export_servers(self):
        """Export server inventory to CSV file."""
        rprint("\n[yellow]Exporting server inventory...[/yellow]")
        try:
            export_path = self.data_manager.export_to_csv()
            rprint(f"[green]✓ Server inventory exported successfully![/green]")
            rprint(f"[blue]📁 Absolute file path:[/blue] [cyan]{export_path}[/cyan]")
        except ValueError as e:
            rprint(f"[red]Error: {str(e)}[/red]")
        except Exception as e:
            rprint(f"[red]An unexpected error occurred: {str(e)}[/red]")
            rprint(f"[dim]Debug traceback: {traceback.format_exc()}[/dim]")

    def exit_program(self):
        rprint("[yellow]Exiting program...[/yellow]")
        sys.exit(0)

if __name__ == "__main__":
    try:
        inventory = ServerInventory()
        inventory.run()
    except Exception as e:
        console.print(f"[red]Fatal error: {str(e)}[/red]")
        rprint(f"[dim]Debug traceback: {traceback.format_exc()}[/dim]")
        sys.exit(1)