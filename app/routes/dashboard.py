from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Order, Product, Customer, Production, Attendance
from app.auth import verify_token
from datetime import datetime, date

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get dashboard summary"""
    today = date.today()
    
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    total_products = db.query(func.count(Product.id)).scalar() or 0
    total_customers = db.query(func.count(Customer.id)).scalar() or 0
    in_production = db.query(func.count(Production.id)).filter(Production.status == "in_progress").scalar() or 0
    pending_orders = db.query(func.count(Order.id)).filter(Order.status == "pending").scalar() or 0
    low_stock = db.query(func.count(Product.id)).filter(Product.stock_quantity < 10).scalar() or 0
    today_attendance = db.query(func.count(Attendance.id)).filter(Attendance.attendance_date == today).scalar() or 0
    
    return {
        "summary": {
            "totalOrders": total_orders,
            "totalProducts": total_products,
            "totalCustomers": total_customers,
            "inProduction": in_production,
            "pendingOrders": pending_orders,
            "lowStockItems": low_stock,
            "todayAttendance": today_attendance
        },
        "timestamp": datetime.utcnow().isoformat()
    }
