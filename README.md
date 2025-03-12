# writer

- create venv
- python -m venv venv


- activate venv
- venv\Scripts\activate



- install requirements
- pip install -r requirements.txt



- run server
- uvicorn app:app --reload

- check if is running
- http://127.0.0.1:8000/ping

- publish 1 article
- http://127.0.0.1:8000/process-article

body

{
  "topic": "Artificial Intelligence in 2025",
  "num_articles": 5,
  "future_dates": true
}

