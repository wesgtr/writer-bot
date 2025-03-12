from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from content_agent import ContentAgent
from clients.wordpress_client import get_categories, publish_post
from settings import Settings

app = FastAPI()
settings = Settings()

class ArticleRequest(BaseModel):
    topic: str
    num_articles: int  # Number of articles to create
    future_dates: bool = False  # If True, schedules the posts for the future

@app.post("/process-article")
def process_article(request: ArticleRequest):
    try:
        topic = request.topic
        num_articles = request.num_articles
        future_dates = request.future_dates

        content_agent = ContentAgent(api_token=settings.OPENAI_API_KEY)

        # Fetch existing categories from WordPress
        categories = get_categories(settings.WORDPRESS_URL)
        category_names = list(categories.values())

        # Set initial publish date
        current_date = datetime.now()
        if future_dates:
            current_date += timedelta(days=1)

        posts = []
        for i in range(num_articles):
            print(f"Processing article {i + 1} for date {current_date.strftime('%Y-%m-%d')}")

            # Generate keywords for the topic
            print("Generating keywords...")
            keywords = content_agent.generate_keywords(topic)
            print("Keywords: Done!")

            # Perform research based on the keywords
            print("Performing research...")
            research_summary = content_agent.research_content(keywords)
            print("Research Summary: Done!")

            # Create an article based on the research
            print("Creating draft article...")
            current_year = datetime.now().year
            draft_article = content_agent.write_article(summary=research_summary, year=current_year)
            print("Draft Article: Done!")

            # Edit and optimize the article
            print("Editing and optimizing article...")
            final_article = content_agent.edit_article(draft_article, category_names)
            print("Final Article: Done!")

            # Select the category
            print("Selecting category...")
            category_id = next((id for id, name in categories.items() if name == final_article["category_name"]), None)
            if category_id is None:
                print(f"Invalid category '{final_article['category_name']}' chosen by AI. Defaulting to the first category.")
                category_id = list(categories.keys())[0]
            print("Category selected.")

            # Generate image (if necessary)
            image_id = None
            if final_article["image_description"]:
                print("Generating image...")
                image_path = content_agent.generate_image(final_article["image_description"])
                image_id = content_agent.upload_image_to_wordpress(image_path)
                print("Image generated and uploaded.")

            # Publish the article on WordPress
            print("Publishing article...")
            post = publish_post(
                title=final_article["title"],
                content=final_article["content"],
                wordpress_url=settings.WORDPRESS_URL,
                publish_date=current_date.strftime('%Y-%m-%dT%H:%M:%S'),
                category_id=category_id,
                featured_media=image_id,
                status="future" if future_dates else "publish"
            )

            print("Publish to WordPress: Done!")
            posts.append(post)

            # Increment date for the next article if scheduling for the future
            if future_dates:
                current_date += timedelta(days=1)

        return {
            "message": "Articles successfully processed and published!",
            "posts": posts
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))