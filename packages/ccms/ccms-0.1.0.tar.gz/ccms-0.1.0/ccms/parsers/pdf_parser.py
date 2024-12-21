import PyPDF2
from rich.console import Console
from .base import BaseParser

console = Console()

class PDFParser(BaseParser):
    def parse(self, file_path: str) -> dict:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                
                return {
                    "full_text": text,
                    "dates": self._extract_dates(text),
                    "sla_metrics": self._extract_sla_metrics(text),
                    "payment_terms": self._extract_payment_terms(text)
                }
        except Exception as e:
            console.print(f"[red]Error parsing PDF: {str(e)}[/red]")
            return {}