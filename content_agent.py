import requests
from prompts import (
    keyword_research_prompt,
    content_research_prompt,
    writing_prompt,
    editing_prompt
)
from clients.open_ai_client import LlmClient
from clients.open_ai_client import generate_image

from clients.wordpress_client import publish_post, publish_image

from settings import Settings

settings = Settings()

class ContentAgent:
    def __init__(self, api_token):
        self.client = LlmClient(api_token)

    def run_agent(self, prompt, input_text):
        try:
            response = self.client.completion(prompt, input_text)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error in run_agent: {e}")
            return None

    def generate_keywords(self, topic):
        return self.run_agent(keyword_research_prompt.format(topic=topic), "")

    def research_content(self, keywords):
        return self.run_agent(content_research_prompt, keywords)

    def write_article(self, summary, year):
        response = self.run_agent(writing_prompt.format(topic=summary, year=year), "")

        parts = response.split("CONTENT:", 1)
        title = parts[0].replace("TITLE:", "").strip() if len(parts) > 1 else "Untitled Article"
        content = parts[1].strip() if len(parts) > 1 else response

        return {"title": title, "content": content}

    def edit_article(self, article_data, categories):
        formatted_categories = ", ".join(categories)
        article_text = f"TITLE: {article_data['title']}\nCONTENT: {article_data['content']}"
        response = self.run_agent(editing_prompt.format(categories=formatted_categories), article_text)

        parts = response.split("CONTENT:", 1)
        title = parts[0].replace("TITLE:", "").strip() if len(parts) > 1 else article_data['title']
        content = parts[1].split("CATEGORY:")[0].strip() if "CATEGORY:" in parts[1] else parts[1].strip()
        category_name = parts[1].split("CATEGORY:")[1].split("IMAGE_DESCRIPTION:")[0].strip() if "CATEGORY:" in parts[
            1] else None
        image_description = parts[1].split("IMAGE_DESCRIPTION:")[1].strip() if "IMAGE_DESCRIPTION:" in parts[
            1] else None

        if category_name not in categories:
            print(f"Invalid category '{category_name}' returned by AI. Defaulting to the first category in the list.")
            category_name = categories[0]

        return {"title": title, "content": content, "category_name": category_name,
                "image_description": image_description}

    def generate_image(self, description):
        return generate_image(description)

    def upload_image_to_wordpress(self, image_path):
        return publish_image(image_path, settings.WORDPRESS_URL)

    @staticmethod
    def publish_to_wordpress(title, content, wordpress_url, publish_date, category_id, status, featured_media=None):
        return publish_post(
            title=title,
            content=content,
            wordpress_url=wordpress_url,
            publish_date=publish_date,
            category_id=category_id,
            featured_media=featured_media,
            status=status
        )
