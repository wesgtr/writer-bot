from fastapi import FastAPI, HTTPException
from routes.article_routes import router as article_router
from settings import Settings
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

settings = Settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SetupRequest(BaseModel):
    topic: str

@app.post("/setup")
def setup_endpoint(request: SetupRequest):
    topic = request.topic
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    try:
        # Example setup logic: Create categories or initialize resources
        # Replace this with your actual setup logic
        print(f"Performing setup for topic: {topic}")
        # Example: Call a function to create categories
        # create_categories(topic)

        return {"message": f"Setup completed for topic: {topic}"}
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=f"An error occurred during setup: {str(e)}")

# Include additional routes
app.include_router(article_router)

@app.get("/ping2")
def ping():
    return {"message": "API2 is running!"}


