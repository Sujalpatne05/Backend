from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routes import (
    auth, products, customers, dashboard, attendance,
    orders, production, expenses, suppliers, stock,
    quotations, payments, accounting, sales, purchases,
    reports, settings as settings_routes, users
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Production Management System API",
    description="🏭 Complete Manufacturing Management Backend",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        settings.FRONTEND_URL,
        settings.VERCEL_FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(dashboard.router)
app.include_router(attendance.router)
app.include_router(orders.router)
app.include_router(production.router)
app.include_router(expenses.router)
app.include_router(suppliers.router)
app.include_router(stock.router)
app.include_router(quotations.router)
app.include_router(payments.router)
app.include_router(accounting.router)
app.include_router(sales.router)
app.include_router(purchases.router)
app.include_router(reports.router)
app.include_router(settings_routes.router)
app.include_router(users.router)

@app.get("/")
async def root():
    """API Root"""
    return {
        "message": "🏭 Production Management System API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "production-management-api"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
