import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    WORDPRESS_URL = os.getenv("WORDPRESS_URL")
    WP_USER = os.getenv("WP_USER")
    PASSWORD = os.getenv("PASSWORD")


if __name__ == "__main__":
    print("OPENAI_API_KEY:", Settings.OPENAI_API_KEY or "Not Found")
    print("WORDPRESS_URL:", Settings.WORDPRESS_URL or "Not Found")
    print("WP_USER:", Settings.WP_USER or "Not Found")
    print("PASSWORD:", Settings.PASSWORD or "Not Found")