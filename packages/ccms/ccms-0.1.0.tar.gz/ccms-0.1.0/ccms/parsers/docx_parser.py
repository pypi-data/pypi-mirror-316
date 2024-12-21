import docx
from rich.console import Console
from .base import BaseParser

console = Console()

class DocxParser(BaseParser):
    def parse(self, file_path: str) -> dict:
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            return {
                "full_text": text,
                "dates": self._extract_dates(text),
                "sla_metrics": self._extract_sla_metrics(text),
                "payment_terms": self._extract_payment_terms(text)
            }
        except Exception as e:
            console.print(f"[red]Error parsing DOCX: {str(e)}[/red]")
            return {}