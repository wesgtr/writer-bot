from content_agent import ContentAgent
from settings import Settings
from prompts import category_generation_prompt
import re

settings = Settings()

from clients.wordpress_client import publish_category


class CategoryCreator:
    def __init__(self, wordpress_url):
        self.wordpress_url = wordpress_url

    @staticmethod
    def generate_category_names(topic):
        content_agent = ContentAgent(api_token=settings.OPENAI_API_KEY)
        category_names = content_agent.run_agent(
            category_generation_prompt.format(topic=topic),
            ""
        )

        if category_names is None:
            print("Error: Failed to generate category names.")
            return []

        clean_category_names = [re.sub(r"^\d+\.\s*", "", name.strip()) for name in category_names.split("\n") if
                                name.strip()]

        return clean_category_names

    def publish_category_to_wordpress(self, category_name):
        return publish_category(
            category_name=category_name,
            wordpress_url=self.wordpress_url
        )

    def create_categories(self, topic):
        category_names = self.generate_category_names(topic)

        created_categories = {}
        for name in category_names:
            response = self.publish_category_to_wordpress(name)
            if response:
                created_categories[response.get("id")] = name

        return created_categories

