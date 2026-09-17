from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth,transaction,categories

app = FastAPI(
    title="Advanced Expense Tracker API",
    description="Enterprise-grade expense tracker with PostgreSQL, multi-currency, and background tasks.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    # allow_credentials=True cannot be combined with wildcard origins (browsers reject it).
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transaction.router)
app.include_router(categories.router)

@app.get("/")
async def root():
    return {"status": "success", "message": "Welcome to the Advanced Expense Tracker API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "postgresql"}