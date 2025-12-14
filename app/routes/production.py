from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Production
from app.auth import verify_token
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

router = APIRouter(prefix="/api/production", tags=["Production"])

class ProductionCreate(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    production_date: date
    notes: Optional[str] = None

class ProductionUpdate(BaseModel):
    status: Optional[str] = None
    completion_date: Optional[date] = None
    notes: Optional[str] = None

class ProductionResponse(BaseModel):
    id: str
    order_id: str
    product_id: str
    quantity: int
    status: str
    production_date: date

@router.get("", response_model=List[ProductionResponse])
async def get_production(
    skip: int = Query(0),
    limit: int = Query(100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get all production records"""
    query = db.query(Production)
    if status:
        query = query.filter(Production.status == status)
    records = query.offset(skip).limit(limit).all()
    return records

@router.post("", response_model=ProductionResponse)
async def create_production(
    production: ProductionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create production record"""
    new_production = Production(
        **production.dict(),
        status="pending",
        created_by=current_user["user_id"]
    )
    db.add(new_production)
    db.commit()
    db.refresh(new_production)
    return new_production

@router.put("/{production_id}", response_model=ProductionResponse)
async def update_production(
    production_id: str,
    production_update: ProductionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Update production record"""
    production = db.query(Production).filter(Production.id == production_id).first()
    if not production:
        raise HTTPException(status_code=404, detail="Production record not found")
    
    update_data = production_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(production, key, value)
    
    db.commit()
    db.refresh(production)
    return production

@router.get("/status/summary")
async def get_production_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get production summary by status"""
    from sqlalchemy import func
    summary = db.query(
        Production.status,
        func.count(Production.id).label("count")
    ).group_by(Production.status).all()
    
    return {
        "summary": [{"status": s[0], "count": s[1]} for s in summary]
    }
