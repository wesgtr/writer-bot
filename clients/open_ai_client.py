import requests
from settings import Settings

settings = Settings()

class LlmClient:
    def __init__(self, api_token, model="gpt-4o-mini"):
        self.api_token = api_token
        self.model = model

    def completion(self, prompt, input_text):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text or ""}
            ],
            "max_tokens": 8000
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("choices")[0]["message"]["content"].strip()

def generate_image(description):
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": description,
        "n": 1,
        "size": "1024x1024"
    }

    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload)

    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        image_path = "generated_image.png"

        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(image_path, "wb") as file:
                file.write(image_response.content)
            return image_path
        else:
            print("Failed to download the image.")
            return None
    else:
        print("Failed to generate image:", response.status_code)
        return None
