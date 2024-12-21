import typer
from typing import Optional
from rich.console import Console
from datetime import datetime
from ccms.parsers.pdf_parser import PDFParser
from ccms.parsers.docx_parser import DocxParser
from ccms.database.supabase_client import get_client
from rich.table import Table

console = Console()

class ContractCommands:
    @staticmethod
    def add_contract(
        file_path: str,
        vendor_name: str,
        contract_type: str,
        start_date: str,
        end_date: str
    ):
        try:
            # Select parser based on file type
            if file_path.endswith('.pdf'):
                parser = PDFParser()
            elif file_path.endswith('.docx'):
                parser = DocxParser()
            else:
                console.print("[red]Unsupported file format. Please provide PDF or DOCX file.[/red]")
                return

            contract_data = parser.parse(file_path)

            # Prepare contract data
            contract_record = {
                "vendor_name": vendor_name,
                "contract_type": contract_type,
                "start_date": start_date,
                "end_date": end_date,
                "contract_data": contract_data,
                "status": "active",
                "created_at": datetime.now().isoformat()
            }

            # Insert into Supabase
            supabase = get_client()
            response = supabase.table("contracts").insert(contract_record).execute()
            
            console.print("[green]Contract successfully added![/green]")
            
        except Exception as e:
            console.print(f"[red]Error adding contract: {str(e)}[/red]")

    @staticmethod
    def list_contracts(vendor: Optional[str] = None, status: Optional[str] = None):
        try:
            supabase = get_client()
            query = supabase.table("contracts").select("*")
            
            if vendor:
                query = query.eq("vendor_name", vendor)
            if status:
                query = query.eq("status", status)

            response = query.execute()
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Vendor")
            table.add_column("Type")
            table.add_column("Start Date")
            table.add_column("End Date")
            table.add_column("Status")

            for contract in response.data:
                table.add_row(
                    contract["vendor_name"],
                    contract["contract_type"],
                    contract["start_date"],
                    contract["end_date"],
                    contract["status"]
                )

            console.print(table)

        except Exception as e:
            console.print(f"[red]Error listing contracts: {str(e)}[/red]")