"""Data categories (target ERP formats) metadata endpoint."""

from typing import Any, Dict, List

from fastapi import APIRouter

from app.agents.tools import CANONICAL_SCHEMAS, get_category_schema
from app.models.schemas import DataCategory

router = APIRouter()


@router.get("/data-categories", response_model=List[Dict[str, Any]])
async def list_data_categories() -> List[Dict[str, Any]]:
    """Return the available target data formats and their canonical schemas."""
    result: List[Dict[str, Any]] = []
    for category in DataCategory:
        if category == DataCategory.OTHER:
            continue
        schema = get_category_schema(category.value)
        description = CANONICAL_SCHEMAS[category.value].get("description", "")
        result.append({
            "value": category.value,
            "label": schema["label"],
            "columns": schema["columns"],
            "description": description,
        })
    return result
