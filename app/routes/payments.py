from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import verify_token
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/payments", tags=["Payments"])

class PaymentCreate(BaseModel):
    invoice_id: str
    amount: float
    payment_method: str
    reference_number: Optional[str] = None

class PaymentUpdate(BaseModel):
    status: Optional[str] = None

@router.get("")
async def get_payments(
    skip: int = Query(0),
    limit: int = Query(100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get all payments"""
    return {
        "message": "Payments list",
        "skip": skip,
        "limit": limit
    }

@router.post("")
async def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create payment"""
    return {
        "message": "Payment recorded",
        "amount": payment.amount,
        "method": payment.payment_method
    }

@router.get("/{payment_id}")
async def get_payment(
    payment_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get payment details"""
    return {"payment_id": payment_id}

@router.put("/{payment_id}")
async def update_payment(
    payment_id: str,
    payment_update: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Update payment"""
    return {"payment_id": payment_id, "status": payment_update.status}
