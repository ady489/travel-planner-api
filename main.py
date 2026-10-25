import os
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, Trip
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Initialize Groq client
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env file")
ai_client = Groq(api_key=api_key)

app = FastAPI()

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request schema
class TripRequest(BaseModel):
    destination: str
    days: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Planner API!"}

@app.post("/plan-trip")
def plan_trip(request: TripRequest, db: Session = Depends(get_db)):
    # 1. Save the initial request to the DB
    new_trip = Trip(destination=request.destination, days=request.days)
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    
    # 2. Build prompt for the AI
    prompt = f"Create a short, bulleted {request.days}-day travel itinerary for {request.destination}. Keep it under 100 words."
    
    try:
        # 3. Generate the itinerary
        chat_completion = ai_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": prompt}
            ],
            model="openai/gpt-oss-20b",
        )
        ai_response = chat_completion.choices[0].message.content
    except Exception as e:
        # If AI fails, we still have the trip saved, but we return an error message
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

    return {
        "status": "success",
        "trip_id": new_trip.id,
        "destination": request.destination,
        "itinerary": ai_response
    }

@app.get("/trips")
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).all()