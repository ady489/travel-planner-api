# Travel Planner API (with AI Integration)

A backend REST API built with FastAPI that generates personalized travel itineraries using AI. It validates user input, saves the trip to a database, and returns a generated day-by-day plan.

## Architecture
*   **Framework:** FastAPI (Python)
*   **Database:** SQLite (via SQLAlchemy)
*   **AI Engine:** Groq API (OpenAI OSS 20b model)
*   **Data Validation:** Pydantic

## Endpoints
*   `GET /` - Welcome message
*   `POST /plan-trip` - Accepts `{"destination": "Paris", "days": 3}`, saves to DB, and returns an AI-generated itinerary.
*   `GET /trips` - Retrieves a list of all previously saved trips.

## How to run locally
1. Clone the repo and navigate into the folder.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file and add your Groq API key:
   ```text
   GROQ_API_KEY=your_key_here
6. Run the server: uvicorn main:app --reload
7. Open http://127.0.0.1:8000/docs to view the interactive Swagger UI.


## What I learned building this:
* How to structure a web API using FastAPI and route decorators.

* How to use Pydantic for robust request data validation.

* How to connect a relational database using SQLAlchemy and manage sessions.

* How to integrate an external LLM API to generate dynamic, context-aware responses.