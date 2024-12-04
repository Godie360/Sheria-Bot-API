from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import chat
from config.settings import settings
from services.db_service import initialize_database

app = FastAPI(title="SHERIA KIGANJANI CHATBOT API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Include chat router only
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.on_event("startup")
async def startup_event():
    """Initialize the database when the application starts"""
    print("Initializing database...")
    initialize_database()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)