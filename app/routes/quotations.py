from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import verify_token
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

router = APIRouter(prefix="/api/quotations", tags=["Quotations"])

class QuotationLineItem(BaseModel):
    product_id: str
    quantity: int
    unit_price: float

class QuotationCreate(BaseModel):
    customer_id: str
    quotation_date: date
    items: List[QuotationLineItem]
    validity_days: Optional[int] = 7
    notes: Optional[str] = None

class QuotationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

@router.get("")
async def get_quotations(
    skip: int = Query(0),
    limit: int = Query(100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get all quotations"""
    return {
        "message": "Quotations endpoint",
        "skip": skip,
        "limit": limit
    }

@router.post("")
async def create_quotation(
    quotation: QuotationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create quotation"""
    return {
        "message": "Quotation created",
        "customer_id": quotation.customer_id,
        "items_count": len(quotation.items)
    }

@router.get("/{quotation_id}")
async def get_quotation(
    quotation_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get single quotation"""
    return {"quotation_id": quotation_id}

@router.put("/{quotation_id}")
async def update_quotation(
    quotation_id: str,
    quotation_update: QuotationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Update quotation"""
    return {"quotation_id": quotation_id, "status": quotation_update.status}

@router.delete("/{quotation_id}")
async def delete_quotation(
    quotation_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Delete quotation"""
    return {"message": "Quotation deleted"}
