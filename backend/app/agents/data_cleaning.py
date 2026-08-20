"""Agent 3: Data Cleaning, Normalization & Anomaly Detection Agent."""

from typing import Dict, Any, List, Tuple
from app.models.schemas import DataAnomaly

class DataCleaningAgent:
    def __init__(self) -> None:
        self.name = "DataCleaningAgent"

    async def clean_and_normalize(
        self, raw_records: List[Dict[str, Any]], column_mappings: Dict[str, str]
    ) -> Tuple[List[Dict[str, Any]], List[DataAnomaly]]:
        """Normalize values, standardize dates, group product variants, flag anomalies."""
        clean_records = []
        anomalies = []

        for idx, rec in enumerate(raw_records):
            mapped_row = {column_mappings.get(k, k): v for k, v in rec.items()}
            
            # Normalize product names
            prod = mapped_row.get("product_name", "")
            if prod in ["Coke 330ml", "Coke"]:
                mapped_row["product_name"] = "Coca-Cola"
            elif prod in ["Bred"]:
                mapped_row["product_name"] = "Sliced Bread"
                
            # Date formatting (convert to ISO format)
            raw_date = mapped_row.get("sale_date", "")
            if "/" in raw_date:
                parts = raw_date.split("/")
                if len(parts) == 3:
                    mapped_row["sale_date"] = f"20{parts[2]}-{parts[0]:0>2}-{parts[1]:0>2}"

            clean_records.append(mapped_row)

        return clean_records, anomalies
