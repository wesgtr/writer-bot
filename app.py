from fastapi import FastAPI
from routes.article_routes import router as article_router

app = FastAPI()

app.include_router(article_router)

@app.get("/ping")
def ping():
    return {"message": "API is running!"}
