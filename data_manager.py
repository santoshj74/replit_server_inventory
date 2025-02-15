import json
import os
import csv
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from datetime import datetime

class DataManager:
    def __init__(self, filename="servers.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def get_servers(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
        except Exception as e:
            raise Exception(f"Error reading server data: {str(e)}")

    def add_server(self, server):
        servers = self.get_servers()

        # Check for duplicate serial number
        if any(s['serial_number'].lower() == server['serial_number'].lower() for s in servers):
            raise ValueError("A server with this serial number already exists")

        servers.append(server)
        self._save_servers(servers)

    def search_servers(self, search_term):
        servers = self.get_servers()
        search_term = search_term.lower()

        return [
            server for server in servers
            if search_term in server['product_name'].lower() or
               search_term in server['serial_number'].lower() or
               search_term in server['rack_location'].lower() or
               search_term in server['username'].lower()
        ]

    def _save_servers(self, servers):
        try:
            with open(self.filename, 'w') as f:
                json.dump(servers, f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving server data: {str(e)}")

    def delete_server(self, serial_number):
        """Delete a server by its serial number."""
        servers = self.get_servers()
        serial_number = serial_number.lower()

        # Find the server with matching serial number
        filtered_servers = [s for s in servers if s['serial_number'].lower() != serial_number]

        if len(filtered_servers) == len(servers):
            raise ValueError("No server found with this serial number")

        self._save_servers(filtered_servers)
        return True

    def export_to_csv(self, export_path=None):
        """Export server data to CSV file."""
        if export_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"server_inventory_{timestamp}.csv"

        # Convert to absolute path
        export_path = os.path.abspath(export_path)

        servers = self.get_servers()
        if not servers:
            raise ValueError("No servers found to export")

        try:
            with open(export_path, 'w', newline='') as csvfile:
                # Define headers
                headers = ["Product Name", "Serial Number", "Rack Location", "Username"]
                writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')

                # Write headers
                writer.writeheader()

                # Write data
                for server in servers:
                    writer.writerow({
                        "Product Name": server['product_name'],
                        "Serial Number": server['serial_number'],
                        "Rack Location": server['rack_location'],
                        "Username": server['username']
                    })
            return export_path
        except Exception as e:
            raise Exception(f"Error exporting to CSV: {str(e)}")