import os
from datetime import datetime, timedelta
from content_agent import ContentAgent
from category_creator import CategoryCreator
from clients.wordpress_client import get_categories, get_published_posts, update_post
from prompts import custom_editing_prompt

from settings import Settings

settings = Settings()

def first_setup(topic):
    category_creator = CategoryCreator(
        wordpress_url=settings.WORDPRESS_URL,
    )
    categories = category_creator.create_categories(topic)
    publish_articles_setup(topic, categories)


def publish_articles_setup(topic, categories=None, future_dates=False):
    if not categories:
        print("No categories provided. Fetching existing categories from WordPress...")
        categories = get_categories(settings.WORDPRESS_URL)
        if not categories:
            print("No categories found on WordPress. Exiting setup.")
            return

    num_articles = int(input("Enter the number of articles to generate: "))

    current_date = datetime.today() + timedelta(days=1) if future_dates else datetime.today()

    for i in range(num_articles):
        article_date = current_date.strftime('%Y-%m-%d')
        print(f"Creating article {i + 1} with date {article_date}")

        status = "future" if future_dates else "publish"
        create_article(topic, current_date, categories, status=status)

        current_date += timedelta(days=1) if future_dates else timedelta(days=-1)

def create_article(topic, publish_date, categories, status="publish"):
    current_year = datetime.now().year
    content_agent = ContentAgent(api_token=settings.OPENAI_API_KEY)

    keywords = content_agent.generate_keywords(topic)
    print("Keywords: Done!")

    research_summary = content_agent.research_content(keywords)
    print("Research Summary: Done!")

    draft_article = content_agent.write_article(summary=research_summary, year=current_year)
    print("Draft Article: Done!")

    category_names = list(categories.values())
    final_article = content_agent.edit_article(draft_article, category_names)
    print("Final Article: Done!")

    category_id = next((id for id, name in categories.items() if name == final_article["category_name"]), None)
    if category_id is None:
        print(f"Invalid category '{final_article['category_name']}' chosen by AI. Defaulting to the first category.")
        category_id = list(categories.keys())[0]

    if final_article["image_description"]:
        image_path = content_agent.generate_image(final_article["image_description"])
        image_id = content_agent.upload_image_to_wordpress(image_path)

        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            print("Local image file deleted successfully.")
    else:
        image_id = None

    ContentAgent.publish_to_wordpress(
        title=final_article["title"],
        content=final_article["content"],
        wordpress_url=settings.WORDPRESS_URL,
        publish_date=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        category_id=category_id,
        featured_media=image_id,
        status=status
    )
    print("Publish to WordPress: Done!")

class TerminalColors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"

def revise_published_posts():
    print(f"{TerminalColors.GREEN}Fetching published posts...{TerminalColors.RESET}")
    published_posts = get_published_posts(settings.WORDPRESS_URL)

    if not published_posts:
        print(f"{TerminalColors.RED}No published posts found.{TerminalColors.RESET}")
        return

    content_agent = ContentAgent(api_token=settings.OPENAI_API_KEY)

    for post in published_posts:
        print(f"Processing post: {post['title']} (ID: {post['id']})")

        original_content = post['content']['rendered']
        revised_content = content_agent.run_agent(custom_editing_prompt, original_content)

        featured_media = post.get('featured_media')
        if not featured_media:
            print(f"{TerminalColors.RED}No image found for this post. Generating an image...{TerminalColors.RESET}")
            image_description = f"Create an image for a blog article titled: '{post['title']}'."

            image_path = content_agent.generate_image(image_description)

            if image_path and os.path.exists(image_path):
                image_id = content_agent.upload_image_to_wordpress(image_path)
                os.remove(image_path)
                print(f"{TerminalColors.GREEN}Image uploaded and local file deleted.{TerminalColors.RESET}")
            else:
                print(f"{TerminalColors.RED}Failed to generate or upload image.{TerminalColors.RESET}")
                image_id = None
        else:
            image_id = featured_media
            print(f"{TerminalColors.GREEN}Image already exists for this post.{TerminalColors.RESET}")

        # Update the post with revised content and image
        try:
            update_post(
                post_id=post['id'],
                wordpress_url=settings.WORDPRESS_URL,
                title=post['title'],
                content=revised_content,
                featured_media=image_id
            )
            print(f"{TerminalColors.GREEN}Post '{post['title']}' updated successfully.{TerminalColors.RESET}")
        except Exception as e:
            print(f"{TerminalColors.RED}Failed to update post '{post['title']}': {e}{TerminalColors.RESET}")


if __name__ == "__main__":
    option = input(
        "Choose an option:\n"
        "1 - First setup, with categories and posts\n"
        "2 - Only generate articles with past dates\n"
        "3 - Only generate articles with future dates\n"
        "4 - Revise all published posts\n"
        "Enter your choice: "
    )
    if option < "4":
        topic = input("Enter the topic for the articles: ")

    if option == "1":
        first_setup(topic)
    elif option == "2":
        publish_articles_setup(topic, future_dates=False)
    elif option == "3":
        publish_articles_setup(topic, future_dates=True)
    elif option == "4":
        revise_published_posts()
    else:
        print("Invalid option selected.")
