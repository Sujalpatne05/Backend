from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Expense, ExpenseCategory
from app.auth import verify_token
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

class ExpenseCreate(BaseModel):
    category_id: str
    amount: float
    description: str
    expense_date: date

class ExpenseUpdate(BaseModel):
    category_id: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: str
    category_id: str
    amount: float
    description: str
    expense_date: date

@router.get("", response_model=List[ExpenseResponse])
async def get_expenses(
    skip: int = Query(0),
    limit: int = Query(100),
    category_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get all expenses"""
    query = db.query(Expense)
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    expenses = query.offset(skip).limit(limit).all()
    return expenses

@router.post("", response_model=ExpenseResponse)
async def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create expense"""
    new_expense = Expense(
        **expense.dict(),
        created_by=current_user["user_id"]
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(
    expense_id: str,
    expense_update: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Update expense"""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_data = expense_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(expense, key, value)
    
    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Delete expense"""
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}

# Expense Categories

class ExpenseCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ExpenseCategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str

@router.get("/categories", response_model=List[ExpenseCategoryResponse])
async def get_expense_categories(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get all expense categories"""
    categories = db.query(ExpenseCategory).filter(ExpenseCategory.status == "active").all()
    return categories

@router.post("/categories", response_model=ExpenseCategoryResponse)
async def create_expense_category(
    category: ExpenseCategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create expense category"""
    new_category = ExpenseCategory(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
