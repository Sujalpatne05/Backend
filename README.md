# Production Management System - Backend API

Fast API Backend for the Production Management System. Complete manufacturing management with authentication, products, orders, customers, and more.

## 📋 Features


## 🚀 Quick Start

### Prerequisites

### Local Development

1. **Clone repository**
```bash
cd "c:\Users\sujal\Desktop\Production Management\production-management-api"
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Create database**
```bash
# Using PostgreSQL
createdb production_management
```

6. **Run server**
```bash
python -m uvicorn app.main:app --reload
```

API will be available at: `http://localhost:8000`  
Docs at: `http://localhost:8000/docs`

### Using Docker

```bash
# Build and run
docker compose up --build

# Run in background
docker compose up -d

# View logs
docker compose logs -f api

# Stop
docker compose down
```

## 📚 API Endpoints

### Authentication
```
POST   /api/auth/login           - User login
POST   /api/auth/register        - User registration
GET    /api/auth/me              - Get current user
```

### Products
```
GET    /api/products             - List all products
GET    /api/products/{id}        - Get product details
POST   /api/products             - Create product
PUT    /api/products/{id}        - Update product
DELETE /api/products/{id}        - Delete product
```

### Customers
```
GET    /api/customers            - List all customers
GET    /api/customers/{id}       - Get customer details
POST   /api/customers            - Create customer
PUT    /api/customers/{id}       - Update customer
DELETE /api/customers/{id}       - Delete customer
```

### Dashboard
```
GET    /api/dashboard/summary    - Dashboard summary
```

### Attendance
```
POST   /api/attendance/checkin   - Check in
POST   /api/attendance/checkout  - Check out
GET    /api/attendance/today     - Get today's attendance
```

## 🔐 Authentication

All protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer <token>
```

## 📝 Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/production_management
JWT_SECRET=your_secret_key_min_32_chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
VERCEL_FRONTEND_URL=https://production-management-system-drab.vercel.app
PORT=8000
DEBUG=True
```

## 🗄️ Database Models


## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app
```

## 📦 Deployment

### Heroku
```bash
# Create Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT app.main:app" > Procfile

# Deploy
git push heroku main
```

### Railway / DigitalOcean
```bash
# Build and push Docker image
docker build -t production-api .
docker push your-registry/production-api
```

## 🐛 Troubleshooting

**Database connection error:**
```bash
# Check PostgreSQL is running
psql -U postgres

# Verify DATABASE_URL in .env
```

**Import errors:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## 📞 Support

For issues or questions, check:

## 📄 License

This project is part of the Production Management System suite.


**Frontend Repository:** [production-management-system](../production-management-system)  
**Status:** ✅ Ready for Development

# Backend

