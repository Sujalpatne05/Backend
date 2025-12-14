from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order, OrderItem, Product, Customer
from app.auth import verify_token
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

router = APIRouter(prefix="/api/orders", tags=["Orders"])

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    order_number: str
    customer_id: str
    order_date: date
    delivery_date: Optional[date] = None
    items: List[OrderItemCreate]
    notes: Optional[str] = None

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    delivery_date: Optional[date] = None
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: str
    order_number: str
    customer_id: str
    total_amount: float
    status: str
    order_date: date

@router.get("", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0),
    limit: int = Query(100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get all orders"""
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    orders = query.offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get single order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create new order"""
    total_amount = 0.0
    
    new_order = Order(
        order_number=order.order_number,
        customer_id=order.customer_id,
        order_date=order.order_date,
        delivery_date=order.delivery_date,
        total_amount=0.0,
        status="pending",
        notes=order.notes,
        created_by=current_user["user_id"]
    )
    db.add(new_order)
    db.flush()
    
    for item in order.items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.quantity * item.unit_price
        )
        db.add(order_item)
        total_amount += order_item.total_price
    
    new_order.total_amount = total_amount
    db.commit()
    db.refresh(new_order)
    return new_order

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: str,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Update order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    update_data = order_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
    
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}")
async def delete_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Delete order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted"}

@router.get("/{order_id}/items")
async def get_order_items(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get order items"""
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return {
        "order_id": order_id,
        "items": [
            {
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price
            }
            for item in items
        ]
    }
