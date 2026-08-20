"""Clients & Learned Mappings endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ClientItem(BaseModel):
    client_id: str
    name: str
    industry: str
    total_migrations: int

@router.get("", response_model=List[ClientItem])
async def list_clients() -> List[ClientItem]:
    return [
        ClientItem(client_id="client_abc_retail", name="ABC Retail Store", industry="Retail", total_migrations=3),
        ClientItem(client_id="client_wellness_clinic", name="Wellness Clinic", industry="Healthcare", total_migrations=1),
    ]

@router.get("/{client_id}/mappings")
async def get_client_mappings(client_id: str) -> Dict[str, Any]:
    return {
        "client_id": client_id,
        "mappings": {
            "Qt.": "quantity",
            "Cust": "customer_name",
            "Prod": "product_name",
        },
        "product_normalizations": {
            "Coca-Cola": ["Coke", "Coca Cola", "Coke 330ml"],
            "Sliced Bread": ["Bred", "Brd"],
        },
    }
