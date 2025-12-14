from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product, ProductCategory
from app.auth import verify_token
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/api/stock", tags=["Stock"])

class StockResponse(BaseModel):
    product_id: str
    name: str
    current_quantity: int
    reorder_level: int
    unit: str
    status: str

@router.get("/summary", response_model=List[StockResponse])
async def get_stock_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get stock summary for all products"""
    products = db.query(Product).filter(Product.status == "active").all()
    return [
        {
            "product_id": p.id,
            "name": p.name,
            "current_quantity": p.quantity,
            "reorder_level": p.reorder_level,
            "unit": p.unit,
            "status": "low" if p.quantity < p.reorder_level else "adequate"
        }
        for p in products
    ]

@router.get("/low-stock")
async def get_low_stock(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get products below reorder level"""
    products = db.query(Product).filter(
        Product.status == "active",
        Product.quantity < Product.reorder_level
    ).all()
    return {
        "low_stock_count": len(products),
        "products": products
    }

@router.put("/{product_id}/adjust")
async def adjust_stock(
    product_id: str,
    adjustment: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Adjust product stock"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    adjustment_qty = adjustment.get("quantity", 0)
    reason = adjustment.get("reason", "manual_adjustment")
    
    product.quantity += adjustment_qty
    db.commit()
    db.refresh(product)
    
    return {
        "product_id": product.id,
        "new_quantity": product.quantity,
        "reason": reason
    }
