from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import verify_token
from typing import Optional

router = APIRouter(prefix="/api/accounting", tags=["Accounting"])

@router.get("/accounts")
async def get_accounts(
    skip: int = Query(0),
    limit: int = Query(100),
    account_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get chart of accounts"""
    return {
        "message": "Chart of Accounts",
        "skip": skip,
        "limit": limit
    }

@router.post("/accounts")
async def create_account(
    account: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create new account"""
    return {"message": "Account created"}

@router.get("/transactions")
async def get_transactions(
    skip: int = Query(0),
    limit: int = Query(100),
    account_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get journal transactions"""
    return {
        "message": "Journal transactions",
        "skip": skip,
        "limit": limit
    }

@router.post("/transactions")
async def create_transaction(
    transaction: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Create journal entry"""
    return {"message": "Transaction recorded"}

@router.get("/trial-balance")
async def get_trial_balance(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get trial balance report"""
    return {
        "debit_total": 0.0,
        "credit_total": 0.0,
        "accounts": []
    }

@router.get("/balance-sheet")
async def get_balance_sheet(
    period: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get balance sheet"""
    return {
        "assets": 0.0,
        "liabilities": 0.0,
        "equity": 0.0
    }

@router.get("/income-statement")
async def get_income_statement(
    period: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get income statement"""
    return {
        "revenue": 0.0,
        "expenses": 0.0,
        "net_income": 0.0
    }
