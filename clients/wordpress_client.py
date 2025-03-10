import base64
import requests
from settings import Settings

settings = Settings()

def get_auth_headers():
    credentials = f"{settings.WP_USER}:{settings.PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode("utf-8")
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }
    return headers

def publish_post(title, content, wordpress_url, publish_date, category_id, status, featured_media=None):
    headers = get_auth_headers()
    url = f"{wordpress_url}/wp-json/wp/v2/posts"
    data = {
        "title": title,
        "content": content,
        "status": status,
        "date": publish_date,
        "categories": [category_id]
    }

    if featured_media:
        data["featured_media"] = featured_media

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Post created successfully!")
        return response.json()
    else:
        print("Failed to create post:", response.status_code)
        try:
            print("Error message:", response.json())
        except ValueError:
            print("Non-JSON error response:", response.text)
        return None


def publish_category(category_name, wordpress_url):
    headers = get_auth_headers()
    url = f"{wordpress_url}/wp-json/wp/v2/categories"
    data = {
        "name": category_name
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Category created successfully!")
        return response.json()
    else:
        print("Failed to create category:", response.status_code)
        try:
            print("Error message:", response.json())
        except ValueError:
            print("Non-JSON error response:", response.text)
        return None

def publish_image(image_path, wordpress_url):
    headers = get_auth_headers()
    headers.pop("Content-Type", None)
    url = f"{wordpress_url}/wp-json/wp/v2/media"

    with open(image_path, 'rb') as img:
        files = {'file': img}
        data = {'status': 'publish'}

        response = requests.post(url, headers=headers, files=files, data=data)

        if response.status_code == 201:
            print("Image uploaded successfully!")
            return response.json().get("id")
        else:
            print("Failed to upload image:", response.status_code)
            try:
                print("Error message:", response.json())
            except ValueError:
                print("Non-JSON error response:", response.text)
            return None

def get_categories(wordpress_url):
    headers = get_auth_headers()
    url = f"{wordpress_url}/wp-json/wp/v2/categories"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        categories = response.json()
        return {category['id']: category['name'] for category in categories}
    else:
        print("Failed to retrieve categories:", response.status_code)
        try:
            print("Error message:", response.json())
        except ValueError:
            print("Non-JSON error response:", response.text)
        return {}

# def get_published_posts(wordpress_url):
#     headers = get_auth_headers()
#     url = f"{wordpress_url}/wp-json/wp/v2/posts?status=publish"
#
#     response = requests.get(url, headers=headers)
#
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print("Failed to fetch published posts:", response.status_code)
#         try:
#             print("Error message:", response.json())
#         except ValueError:
#             print("Non-JSON error response:", response.text)
#         return []

def get_published_posts(wordpress_url):
    headers = get_auth_headers()
    all_posts = []
    page = 1
    per_page = 100

    while True:
        url = f"{wordpress_url}/wp-json/wp/v2/posts?status=publish&per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            posts = response.json()
            if not posts:
                break
            all_posts.extend(posts)
            page += 1
        elif response.status_code == 400 and "rest_post_invalid_page_number" in response.text:
            break
        else:
            print("Failed to fetch published posts:", response.status_code)
            try:
                print("Error message:", response.json())
            except ValueError:
                print("Non-JSON error response:", response.text)
            break

    return all_posts

def update_post(post_id, wordpress_url, title, content, featured_media=None):
    headers = get_auth_headers()
    url = f"{wordpress_url}/wp-json/wp/v2/posts/{post_id}"
    data = {
        "title": title,
        "content": content,
    }

    if featured_media:
        data["featured_media"] = featured_media

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Post {post_id} updated successfully.")
        return response.json()
    else:
        print(f"Failed to update post {post_id}: {response.status_code}")
        try:
            print("Error message:", response.json())
        except ValueError:
            print("Non-JSON error response:", response.text)
        return None