import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    WORDPRESS_URL = os.getenv("WORDPRESS_URL")
    WP_USER = os.getenv("WP_USER")
    PASSWORD = os.getenv("PASSWORD")
