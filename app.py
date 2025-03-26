from fastapi import FastAPI
from routes.article_routes import router as article_router
from settings import Settings

settings = Settings()

app = FastAPI()

app.include_router(article_router)

@app.get("/ping2")
def ping():
    return {"message": "API2 is running!"}
