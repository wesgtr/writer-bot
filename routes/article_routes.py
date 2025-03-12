from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from content_agent import ContentAgent
from clients.wordpress_client import get_categories, publish_post
from settings import Settings

router = APIRouter()
settings = Settings()

class ArticleRequest(BaseModel):
    topic: str
    num_articles: int
    future_dates: bool = False

@router.post("/process-article")
def process_article(request: ArticleRequest):
    try:
        topic = request.topic
        num_articles = request.num_articles
        future_dates = request.future_dates

        content_agent = ContentAgent(api_token=settings.OPENAI_API_KEY)

        categories = get_categories(settings.WORDPRESS_URL)
        category_names = list(categories.values())

        current_date = datetime.now()
        if future_dates:
            current_date += timedelta(days=1)

        posts = []
        for i in range(num_articles):
            print(f"Processing article {i + 1} for date {current_date.strftime('%Y-%m-%d')}")

            keywords = content_agent.generate_keywords(topic)
            research_summary = content_agent.research_content(keywords)
            draft_article = content_agent.write_article(summary=research_summary, year=datetime.now().year)
            final_article = content_agent.edit_article(draft_article, category_names)

            category_id = next((id for id, name in categories.items() if name == final_article["category_name"]), None)
            if category_id is None:
                category_id = list(categories.keys())[0]

            image_id = None
            if final_article["image_description"]:
                image_path = content_agent.generate_image(final_article["image_description"])
                image_id = content_agent.upload_image_to_wordpress(image_path)

            post = publish_post(
                title=final_article["title"],
                content=final_article["content"],
                wordpress_url=settings.WORDPRESS_URL,
                publish_date=current_date.strftime('%Y-%m-%dT%H:%M:%S'),
                category_id=category_id,
                featured_media=image_id,
                status="future" if future_dates else "publish"
            )

            posts.append(post)

            if future_dates:
                current_date += timedelta(days=1)

        return {"message": "Articles successfully processed and published!", "posts": posts}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
