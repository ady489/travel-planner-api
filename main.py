import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, Trip
from dotenv import load_dotenv
from groq import Groq

# Load the API key
load_dotenv()
ai_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TripRequest(BaseModel):
    destination: str
    days: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Planner API!"}

@app.post("/plan-trip")
def plan_trip(request: TripRequest, db: Session = Depends(get_db)):
    # 1. Save to DB
    new_trip = Trip(destination=request.destination, days=request.days)
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    
    # 2. Generate the itinerary using Groq AI
    prompt = f"Create a short, bulleted {request.days}-day travel itinerary for {request.destination}. Keep it under 100 words."
    
    chat_completion = ai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": prompt}
        ],
        model="openai/gpt-oss-20b", # A fast, free model
    )
    
    ai_response = chat_completion.choices[0].message.content
    
    # 3. Return the trip details and the AI plan
    return {
        "status": "success",
        "trip_id": new_trip.id,
        "destination": request.destination,
        "itinerary": ai_response
    }

@app.get("/trips")
def get_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).all()
    return trips