from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import verify_token
from typing import Optional

router = APIRouter(prefix="/api/sales", tags=["Sales"])

@router.get("")
async def get_sales(
    skip: int = Query(0),
    limit: int = Query(100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get all sales orders"""
    return {"message": "Sales orders list"}

@router.post("")
async def create_sales_order(
    order: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create sales order"""
    return {"message": "Sales order created"}

@router.get("/summary")
async def get_sales_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get sales summary"""
    return {
        "total_sales": 0.0,
        "pending_orders": 0,
        "completed_orders": 0
    }

@router.get("/reports")
async def get_sales_reports(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get sales reports"""
    return {"reports": []}
