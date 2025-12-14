from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Attendance, User
from app.auth import verify_token
from pydantic import BaseModel
from datetime import datetime, date

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])

class AttendanceCheckIn(BaseModel):
    employee_id: str

class AttendanceCheckOut(BaseModel):
    employee_id: str
    notes: str = ""

@router.post("/checkin")
async def check_in(
    request: AttendanceCheckIn,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Employee check-in"""
    today = date.today()
    
    existing = db.query(Attendance).filter(
        Attendance.employee_id == request.employee_id,
        Attendance.attendance_date == today
    ).first()
    
    if existing and existing.check_in_time:
        raise HTTPException(status_code=409, detail="Already checked in today")
    
    attendance = Attendance(
        employee_id=request.employee_id,
        check_in_time=datetime.utcnow(),
        attendance_date=today,
        status="present"
    )
    
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    
    return {
        "message": "Checked in successfully",
        "check_in_time": attendance.check_in_time.isoformat()
    }

@router.post("/checkout")
async def check_out(
    request: AttendanceCheckOut,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Employee check-out"""
    today = date.today()
    
    attendance = db.query(Attendance).filter(
        Attendance.employee_id == request.employee_id,
        Attendance.attendance_date == today
    ).first()
    
    if not attendance:
        raise HTTPException(status_code=404, detail="No check-in found for today")
    
    if attendance.check_out_time:
        raise HTTPException(status_code=409, detail="Already checked out today")
    
    attendance.check_out_time = datetime.utcnow()
    attendance.notes = request.notes
    db.commit()
    
    return {
        "message": "Checked out successfully",
        "check_out_time": attendance.check_out_time.isoformat()
    }

@router.get("/today")
async def get_today_attendance(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get today's attendance"""
    today = date.today()
    attendance_records = db.query(Attendance).filter(Attendance.attendance_date == today).all()
    
    return {
        "date": today.isoformat(),
        "records": [
            {
                "id": a.id,
                "employeeId": a.employee_id,
                "checkInTime": a.check_in_time.isoformat() if a.check_in_time else None,
                "checkOutTime": a.check_out_time.isoformat() if a.check_out_time else None,
                "status": a.status
            }
            for a in attendance_records
        ]
    }
