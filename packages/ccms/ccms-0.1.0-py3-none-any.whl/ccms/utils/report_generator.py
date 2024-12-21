import json
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()

class ReportGenerator:
    @staticmethod
    def generate_report(compliance_status: dict):
        report_path = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(compliance_status, f, indent=4)
        console.print(f"[green]Compliance report generated: {report_path}[/green]")

    @staticmethod
    def display_status(compliance_status: dict):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Check Type")
        table.add_column("Status")
        table.add_column("Details")

        checks = compliance_status["checks"]
        for check_type, check_data in checks.items():
            table.add_row(
                check_type,
                check_data["status"],
                check_data["details"]
            )

        console.print(table)