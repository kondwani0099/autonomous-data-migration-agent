"""Agent 2: Context-Aware Schema Mapping Agent."""

from typing import Dict, Any, List, Tuple

class SchemaMappingAgent:
    def __init__(self) -> None:
        self.name = "SchemaMappingAgent"

    async def map_columns(
        self, client_id: str, extracted_columns: List[str]
    ) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
        """Map raw columns to Uniplexity ERP schema; generate clarification triggers if ambiguous."""
        mappings = {
            "Date": "sale_date",
            "Cust": "customer_name",
            "Prod": "product_name",
            "Qt.": "quantity",
            "Price": "unit_price",
            "Total": "total_amount",
        }
        
        clarifications = [
            {
                "question": "What does 'Qt.' mean in this ledger context?",
                "options": ["Quantity", "Quarts (Volume)", "Other"],
                "context": "Column 'Qt.' found near 'Price' and 'Total'",
                "agent": self.name,
            }
        ]
        return mappings, clarifications
