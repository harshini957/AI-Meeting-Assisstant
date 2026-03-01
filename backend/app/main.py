from fastapi import FastAPI
from app.core.database import engine, Base
from app.models.meeting import Meeting
from app.routes.meeting_routes import router as meeting_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(meeting_router)


@app.get("/")
def root():
    return {"message": "Backend running"}