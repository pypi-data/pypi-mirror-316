from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> dict:
        pass
    
    def _extract_dates(self, text: str) -> list:
        return []
    
    def _extract_sla_metrics(self, text: str) -> list:
        return []
    
    def _extract_payment_terms(self, text: str) -> list:
        return []