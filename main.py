
import uvicorn
from fastapi import FastAPI

from api.routers import chat_web, chat_whatsapp
from core.config import settings
from storage.database import engine, Base

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Customer Support",
    description="A production-ready AI-powered customer support automation system.",
    version="1.0.0",
)

# Include API routers
app.include_router(chat_web.router, prefix="/api/v1", tags=["Web Chat"])
app.include_router(chat_whatsapp.router, prefix="/api/v1", tags=["WhatsApp Chat"])

@app.get("/", tags=["Health Check"])
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
