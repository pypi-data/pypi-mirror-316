from rich.console import Console
from ccms.database.supabase_client import get_client
from ccms.utils.compliance_checker import ComplianceChecker
from ccms.utils.report_generator import ReportGenerator
from datetime import datetime

console = Console()

class ComplianceCommands:
    @staticmethod
    def check_compliance(contract_id: str, generate_report: bool = False):
        try:
            supabase = get_client()
            response = supabase.table("contracts").select("*").eq("id", contract_id).execute()
            
            if not response.data:
                console.print("[red]Contract not found![/red]")
                return

            contract = response.data[0]
            
            compliance_status = {
                "contract_id": contract_id,
                "checks": {
                    "document_validity": ComplianceChecker.check_document_validity(contract),
                    "sla_compliance": ComplianceChecker.check_sla_compliance(contract),
                    "payment_compliance": ComplianceChecker.check_payment_compliance(contract)
                },
                "check_date": datetime.now().isoformat()
            }

            supabase.table("compliance_checks").insert(compliance_status).execute()

            if generate_report:
                ReportGenerator.generate_report(compliance_status)
            else:
                ReportGenerator.display_status(compliance_status)

        except Exception as e:
            console.print(f"[red]Error checking compliance: {str(e)}[/red]")
