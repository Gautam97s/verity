from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from config import settings
    from db import init_db
    from routers import ingest, cashflow, actions, insights, business, pitchdeck, enrichment, risk, forecast, reports, webhooks
except ImportError:
    from .config import settings
    from .db import init_db
    from .routers import ingest, cashflow, actions, insights, business, pitchdeck, enrichment, risk, forecast, reports, webhooks


app = FastAPI(title="Verity API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to Verity API"}

# Register routes
app.include_router(business.router, prefix="/business", tags=["Business"])
app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(enrichment.router, prefix="/enrichment", tags=["Enrichment"])
app.include_router(risk.router, prefix="/risk", tags=["Risk"])
app.include_router(insights.router, prefix="/insights", tags=["Insights"])
app.include_router(actions.router, prefix="/actions", tags=["Actions"])
app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(pitchdeck.router, prefix="/pitchdeck", tags=["Pitchdeck"])
app.include_router(cashflow.router, prefix="/cashflow", tags=["Cashflow"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
