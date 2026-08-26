"""Shared ADK tool functions for the Uniplexity migration agent swarm.

Each function is a plain Python callable with type hints, designed to be
wrapped in a ``google.adk.tools.FunctionTool`` and attached to an
``LlmAgent``. This mirrors the pattern from the reference article
"Building AI Agents with Google ADK, FastAPI, and MCP".
"""

from __future__ import annotations

import datetime
import re
from typing import Any, Dict, List, Tuple

from app.models.schemas import DataAnomaly, DataCategory, DocumentType


# ---------------------------------------------------------------------------
# Canonical ERP schemas per data category
# ---------------------------------------------------------------------------
CANONICAL_SCHEMAS: Dict[str, Dict[str, Any]] = {
    DataCategory.SALES.value: {
        "label": "Sales",
        "description": "Sales ledger records: what was sold, to whom, and for how much.",
        "columns": [
            "sale_date", "customer_name", "product_name", "quantity", "unit_price", "total_amount",
        ],
        "keywords": {
            "sale_date": ["date", "dt", "day", "sales date"],
            "customer_name": ["cust", "customer", "client", "account", "buyer"],
            "product_name": ["prod", "product", "item", "sku", "description"],
            "quantity": ["qty", "qt", "quantity", "units", "qty sold"],
            "unit_price": ["price", "unit price", "rate", "cost"],
            "total_amount": ["total", "amount", "value", "subtotal"],
        },
    },
    DataCategory.EXPENSES.value: {
        "label": "Expenses",
        "description": "Business expenses: payments to vendors for goods and services.",
        "columns": [
            "expense_date", "vendor_name", "category", "description", "amount",
        ],
        "keywords": {
            "expense_date": ["date", "dt", "expense date", "paid on"],
            "vendor_name": ["vendor", "payee", "supplier", "merchant", "name", "paid to"],
            "category": ["category", "type", "gl account", "account", "department"],
            "description": ["description", "details", "note", "memo", "purpose"],
            "amount": ["amount", "total", "value", "debit", "cost"],
        },
    },
    DataCategory.PAYROLL.value: {
        "label": "Payroll",
        "description": "Employee payroll: hours worked, rates, gross and net pay.",
        "columns": [
            "pay_date", "employee_name", "role", "hours_worked", "hourly_rate",
            "gross_pay", "deductions", "net_pay",
        ],
        "keywords": {
            "pay_date": ["date", "pay date", "period", "payroll date"],
            "employee_name": ["employee", "name", "staff", "worker", "person"],
            "role": ["role", "position", "title", "job", "department"],
            "hours_worked": ["hours", "time", "hrs", "hours worked"],
            "hourly_rate": ["rate", "hourly", "wage", "hourly rate"],
            "gross_pay": ["gross", "gross pay", "earnings", "salary"],
            "deductions": ["deduction", "tax", "withholding", "deductions"],
            "net_pay": ["net", "net pay", "take home", "paid"],
        },
    },
    DataCategory.INVOICES.value: {
        "label": "Invoices",
        "description": "Customer invoices: amounts billed, taxes and totals due.",
        "columns": [
            "invoice_date", "invoice_number", "customer_name", "due_date",
            "subtotal", "tax", "total_due",
        ],
        "keywords": {
            "invoice_date": ["invoice date", "date", "issued", "created"],
            "invoice_number": ["invoice", "invoice no", "inv #", "number", "no."],
            "customer_name": ["customer", "client", "bill to", "account", "company"],
            "due_date": ["due", "due date", "payment due", "payable by"],
            "subtotal": ["subtotal", "sub total", "sub-total"],
            "tax": ["tax", "vat", "gst", "sales tax"],
            "total_due": ["total", "total due", "amount due", "balance", "total amount"],
        },
    },
    DataCategory.PURCHASES.value: {
        "label": "Purchases",
        "description": "Purchase orders: goods bought from suppliers and their costs.",
        "columns": [
            "purchase_date", "supplier_name", "item_name", "quantity", "unit_cost", "total_cost",
        ],
        "keywords": {
            "purchase_date": ["date", "purchase date", "po date", "ordered"],
            "supplier_name": ["supplier", "vendor", "seller", "name", "supplier name"],
            "item_name": ["item", "product", "description", "material", "goods"],
            "quantity": ["qty", "quantity", "units", "qty purchased"],
            "unit_cost": ["unit cost", "cost", "price", "rate", "unit price"],
            "total_cost": ["total", "amount", "total cost", "value", "subtotal"],
        },
    },
    DataCategory.OTHER.value: {
        "label": "Other",
        "columns": [],
        "keywords": {},
    },
}

# Date + numeric fields that should be normalized per category
CATEGORY_DATE_FIELDS: Dict[str, str] = {
    DataCategory.SALES.value: "sale_date",
    DataCategory.EXPENSES.value: "expense_date",
    DataCategory.PAYROLL.value: "pay_date",
    DataCategory.INVOICES.value: "invoice_date",
    DataCategory.PURCHASES.value: "purchase_date",
}

CATEGORY_EXTRA_DATE_FIELDS: Dict[str, List[str]] = {
    DataCategory.INVOICES.value: ["due_date"],
}

CATEGORY_NUMERIC_FIELDS: Dict[str, List[str]] = {
    DataCategory.SALES.value: ["quantity", "unit_price", "total_amount"],
    DataCategory.EXPENSES.value: ["amount"],
    DataCategory.PAYROLL.value: ["hours_worked", "hourly_rate", "gross_pay", "deductions", "net_pay"],
    DataCategory.INVOICES.value: ["subtotal", "tax", "total_due"],
    DataCategory.PURCHASES.value: ["quantity", "unit_cost", "total_cost"],
    DataCategory.OTHER.value: [],
}


def get_category_schema(data_category: str) -> Dict[str, Any]:
    """Return the canonical target schema (columns + label) for a data category."""
    schema = CANONICAL_SCHEMAS.get(data_category, CANONICAL_SCHEMAS[DataCategory.OTHER.value])
    return {"label": schema["label"], "columns": schema["columns"]}


def _normalize_column_name(name: str) -> str:
    """Lowercase and strip punctuation for fuzzy matching."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


# ---------------------------------------------------------------------------
# Agent 1: Document Understanding tools
# ---------------------------------------------------------------------------
def extract_document_columns(file_path: str, file_type: str) -> Dict[str, Any]:
    """Extract column headers and classify a legacy document.

    Args:
        file_path: Path or GCS URI of the uploaded document.
        file_type: MIME/extension type (e.g. 'csv', 'xlsx', 'pdf', 'png').

    Returns:
        A dict with ``document_type``, ``detected_columns``, and
        ``confidence_score``.
    """
    # In production this would call Gemini multimodal understanding.
    # Here we return a deterministic mock for the sales-ledger sample.
    return {
        "document_type": DocumentType.SALES_LEDGER.value,
        "detected_columns": ["Date", "Cust", "Prod", "Qt.", "Price", "Total"],
        "confidence_score": 0.92,
    }


def extract_raw_records(file_path: str, file_type: str) -> List[Dict[str, Any]]:
    """Extract raw tabular records from a legacy document.

    Args:
        file_path: Path or GCS URI of the uploaded document.
        file_type: MIME/extension type.

    Returns:
        A list of raw record dicts keyed by the detected column headers.
    """
    return [
        {"Date": "01/15/24", "Cust": "ABC Store", "Prod": "Coke 330ml", "Qt.": "10", "Price": "1.50", "Total": "15.00"},
        {"Date": "01/15/24", "Cust": "ABC Store", "Prod": "Coca-Cola", "Qt.": "5", "Price": "1.50", "Total": "7.50"},
        {"Date": "01/16/24", "Cust": "XYZ Market", "Prod": "Bred", "Qt.": "20", "Price": "2.00", "Total": "40.00"},
    ]


# ---------------------------------------------------------------------------
# Agent 2: Schema Mapping tools (category-aware)
# ---------------------------------------------------------------------------
def map_columns_to_schema(
    client_id: str, extracted_columns: List[str], data_category: str = DataCategory.SALES.value
) -> Dict[str, Any]:
    """Map raw document columns to the canonical schema for the selected data category.

    Args:
        client_id: Target client identifier.
        extracted_columns: Column headers detected by the document agent.
        data_category: Target ERP data format (sales, expenses, payroll, invoices, purchases).

    Returns:
        A dict with ``mappings`` (raw -> canonical), ``schema`` (target columns),
        and ``clarifications`` (list of human-in-the-loop questions when confidence is low).
    """
    schema = get_category_schema(data_category)
    keywords = CANONICAL_SCHEMAS.get(data_category, {}).get("keywords", {})

    # Build a reverse index: normalized keyword -> canonical column
    keyword_index: Dict[str, str] = {}
    for canonical, kws in keywords.items():
        for kw in kws:
            keyword_index[_normalize_column_name(kw)] = canonical

    mappings: Dict[str, str] = {}
    clarifications: List[Dict[str, Any]] = []
    used_canonical: set = set()

    for col in extracted_columns:
        norm = _normalize_column_name(col)
        matched = keyword_index.get(norm)

        # Partial / substring fallback
        if not matched:
            for kw, canonical in keyword_index.items():
                if kw and (kw in norm or norm in kw):
                    matched = canonical
                    break

        if matched and matched not in used_canonical:
            mappings[col] = matched
            used_canonical.add(matched)
        elif matched and matched in used_canonical:
            # Duplicate target; keep as-is and ask
            clarifications.append({
                "question": f"Column '{col}' looks like it maps to '{matched}', but that field is already used. How should '{col}' be treated?",
                "options": ["Skip this column", "Overwrite existing mapping", "Other"],
                "context": f"Column '{col}' in a {schema['label'].lower()} dataset",
                "agent": "SchemaMappingAgent",
            })
        else:
            clarifications.append({
                "question": f"What does column '{col}' represent in this {schema['label'].lower()} data?",
                "options": [schema["label"], "Skip this column", "Other"],
                "context": f"Unrecognized column '{col}' for target format '{schema['label']}'",
                "agent": "SchemaMappingAgent",
            })

    return {"mappings": mappings, "schema": schema, "clarifications": clarifications}


# ---------------------------------------------------------------------------
# Agent 3: Data Cleaning & Normalization tools (category-aware)
# ---------------------------------------------------------------------------
def normalize_product_name(product_name: str) -> str:
    """Normalize product name variants to a canonical form."""
    variants = {
        "Coke 330ml": "Coca-Cola",
        "Coke": "Coca-Cola",
        "Bred": "Sliced Bread",
        "Coca Cola": "Coca-Cola",
        "Coca-Cola 330ml": "Coca-Cola",
    }
    return variants.get(product_name, product_name)


def normalize_date(raw_date: str) -> str:
    """Convert a legacy date string to ISO 8601 (YYYY-MM-DD)."""
    if raw_date is None:
        return raw_date
    raw_date = str(raw_date).strip()
    if "/" in raw_date:
        parts = raw_date.split("/")
        if len(parts) == 3:
            try:
                year = int(parts[2])
                if year < 100:
                    year += 2000
                return f"{year:04d}-{int(parts[0]):02d}-{int(parts[1]):02d}"
            except ValueError:
                return raw_date
    elif "-" in raw_date:
        parts = raw_date.split("-")
        if len(parts) == 3 and len(parts[2]) == 2:
            try:
                return f"20{parts[2]}-{int(parts[0]):02d}-{int(parts[1]):02d}"
            except ValueError:
                return raw_date
    return raw_date


def normalize_amount(value: Any) -> Any:
    """Parse currency strings like '$1,234.56' / '1.50' into float, else return original."""
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace(",", "").replace("$", "").replace(" ", "")
    if not s:
        return value
    try:
        return float(s)
    except ValueError:
        return value


def clean_and_normalize_records(
    raw_records: List[Dict[str, Any]],
    column_mappings: Dict[str, str],
    data_category: str = DataCategory.SALES.value,
) -> Dict[str, Any]:
    """Normalize values, standardize dates, and flag anomalies for the target category.

    Args:
        raw_records: Records as extracted by the document agent.
        column_mappings: Raw -> canonical column mapping.
        data_category: Target ERP data format guiding normalization rules.

    Returns:
        A dict with ``clean_records`` and ``anomalies``.
    """
    clean_records: List[Dict[str, Any]] = []
    anomalies: List[Dict[str, Any]] = []

    date_field = CATEGORY_DATE_FIELDS.get(data_category)
    extra_date_fields = CATEGORY_EXTRA_DATE_FIELDS.get(data_category, [])
    numeric_fields = CATEGORY_NUMERIC_FIELDS.get(data_category, [])

    # Fields that represent names should be title-cased
    name_fields = {
        "customer_name", "vendor_name", "supplier_name", "employee_name", "product_name", "item_name",
    }

    for idx, rec in enumerate(raw_records):
        mapped_row = {column_mappings.get(k, k): v for k, v in rec.items()}

        # Normalize name fields
        for field in name_fields:
            if field in mapped_row and mapped_row[field] is not None:
                mapped_row[field] = str(mapped_row[field]).strip()

        # Normalize product/item names
        for field in ("product_name", "item_name"):
            if field in mapped_row and mapped_row[field] is not None:
                mapped_row[field] = normalize_product_name(str(mapped_row[field]))

        # Normalize date fields
        if date_field and mapped_row.get(date_field) is not None:
            mapped_row[date_field] = normalize_date(mapped_row.get(date_field))
        for extra in extra_date_fields:
            if mapped_row.get(extra) is not None:
                mapped_row[extra] = normalize_date(mapped_row.get(extra))

        # Normalize numeric fields and flag anomalies
        for field in numeric_fields:
            if field in mapped_row and mapped_row[field] is not None:
                original = mapped_row[field]
                mapped_row[field] = normalize_amount(original)
                if isinstance(mapped_row[field], str):
                    anomalies.append({
                        "record_index": idx,
                        "field": field,
                        "reason": "Non-numeric value",
                        "severity": "error",
                        "value": original,
                    })

        clean_records.append(mapped_row)

    return {"clean_records": clean_records, "anomalies": anomalies}


# ---------------------------------------------------------------------------
# Agent 4: Validation & Import tools
# ---------------------------------------------------------------------------
def generate_dry_run_preview(
    job_id: str,
    clean_records: List[Dict[str, Any]],
    anomalies: List[DataAnomaly],
    target_schema: Optional[Dict[str, Any]] = None,
    mappings: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Generate a dry-run preview before human approval."""
    schema = target_schema or get_category_schema(DataCategory.SALES.value)
    return {
        "job_id": job_id,
        "total_records": len(clean_records),
        "clean_count": len(clean_records) - len(anomalies),
        "anomalies": [a.model_dump() if hasattr(a, "model_dump") else a for a in anomalies],
        "sample_records": clean_records[:50],
        "records": clean_records,
        "audit_trail": [],
        "target_schema": schema,
        "mappings": mappings or [],
    }


def commit_records_to_erp(
    job_id: str, clean_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Commit validated records to the target Uniplexity ERP database."""
    return {"job_id": job_id, "imported_records": len(clean_records)}