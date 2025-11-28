from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from db import init_db
from routers import ingest, cashflow, actions, insights, business
from routers import pitchdeck

app = FastAPI(title="Verity Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

# Register routes
app.include_router(business.router, prefix="/business", tags=["Business"])
app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(cashflow.router, prefix="/cashflow", tags=["Cashflow"])
app.include_router(insights.router, prefix="/insights", tags=["Insights"])
app.include_router(actions.router, prefix="/actions", tags=["Actions"])
app.include_router(pitchdeck.router, prefix="/pitchdeck", tags=["Pitchdeck"])
