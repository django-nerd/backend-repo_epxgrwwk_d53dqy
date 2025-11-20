import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database import db, create_document
from schemas import ContactMessage

app = FastAPI(title="Interactive Map Landing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Interactive Map Landing Backend Running"}

@app.get("/test")
def test_database():
    """Quick database connectivity check"""
    status: Dict[str, Any] = {
        "backend": "ok",
        "database": "disconnected",
    }
    try:
        if db is not None:
            db.list_collection_names()
            status["database"] = "ok"
        else:
            status["database"] = "missing_env"
    except Exception as e:
        status["database_error"] = str(e)
    return status

@app.post("/contact")
async def submit_contact(msg: ContactMessage):
    """Store contact/support messages in the database"""
    try:
        inserted_id = create_document("contactmessage", msg)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        # If database isn't configured, still respond gracefully for landing usage
        return {"status": "received", "note": "db_unavailable", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
