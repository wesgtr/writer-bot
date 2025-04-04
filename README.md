# Bot Writer API

## Project Presentation
Our project is an API that uses artificial intelligence to generate personalized blog articles. The idea came from the need to automate content creation, which usually takes time and creativity. We use the OpenAI API as an intelligent agent (AI agent) that researches and writes articles based on the user’s chosen topic.

## What is an AI Agent?
An AI agent is like a smart assistant that can make decisions, complete tasks, and respond to commands independently. In our project, the AI agent:

- Searches information about the given topic
- Writes articles with proper structure and tone
- Adapts the content based on each user's preferences (style, category, etc.)

## (Currently in progress not fully implemented) Why We Created User Accounts and Settings
Originally, the bot worked for only one blog. To make it scalable and useful for multiple users, we added:

- User authentication and login
- Personalized settings for content preferences
- Storage for generated articles linked to user accounts

## About Future Connections Beyond WordPress
While we currently support WordPress, we are building the system in a flexible way, so in the future it can also connect to:

- Other blogging platforms (like Medium, Ghost, LinkedIn)
- E-commerce sites (for product descriptions)
- Cloud-based tools (like Google Docs or Notion)
- Internal company systems via webhooks or APIs

## Technical Summary
- **Back-end:** FastAPI (Python)
- **Database:** MySQL (for users and blog settings)
- **AI:** OpenAI API (GPT models to generate blog content)

## Setup Instructions

### Create a Virtual Environment
```sh
python -m venv venv
```

### Activate Virtual Environment
#### Windows
```sh
venv\Scripts\activate
```
#### Mac/Linux
```sh
source venv/bin/activate
```

### Install Requirements
```sh
pip install -r requirements.txt
```

### Run the Server
```sh
uvicorn app:app --reload
```

### Check If the Server is Running
Open a browser and go to:
```
http://127.0.0.1:8000/ping
```

### Publish an Article
Send a POST request to:
```
http://127.0.0.1:8000/process-article
```

#### Request Body Example:
```json
{
  "topic": "Artificial Intelligence in 2025",
  "num_articles": 5,
  "future_dates": true
}
```

