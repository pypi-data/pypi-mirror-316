import typer
from ccms.commands.contract_commands import ContractCommands
from ccms.commands.compliance_commands import ComplianceCommands
from typing import Optional

app = typer.Typer()

@app.command()
def add_contract(
    file_path: str = typer.Argument(..., help="Path to contract file (PDF/DOCX)"),
    vendor_name: str = typer.Option(..., "--vendor", "-v", help="Vendor name"),
    contract_type: str = typer.Option(..., "--type", "-t", help="Contract type"),
    start_date: str = typer.Option(..., "--start", "-s", help="Contract start date (YYYY-MM-DD)"),
    end_date: str = typer.Option(..., "--end", "-e", help="Contract end date (YYYY-MM-DD)")
):
    """Add a new contract to the system."""
    ContractCommands.add_contract(file_path, vendor_name, contract_type, start_date, end_date)

@app.command()
def list_contracts(
    vendor: Optional[str] = typer.Option(None, "--vendor", "-v", help="Filter by vendor name"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by contract status")
):
    """List all contracts with optional filters."""
    ContractCommands.list_contracts(vendor, status)

@app.command()
def check_compliance(
    contract_id: str = typer.Argument(..., help="Contract ID to check compliance"),
    generate_report: bool = typer.Option(False, "--report", "-r", help="Generate compliance report")
):
    """Check compliance status for a specific contract."""
    ComplianceCommands.check_compliance(contract_id, generate_report)

if __name__ == "__main__":
    app()

