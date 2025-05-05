# Weather Chatbot using Dialogflow & FastAPI

This project is a webhook-based weather chatbot using **Google Dialogflow ES** and **FastAPI**, capable of providing:

- Current weather for any global city
- Multiple days forecast weather info for a city (limited to ~8 unique days)

---

## Features

- Integrates with Dialogflow ES using webhook
- Fetches data from OpenWeatherMap API
- Supports four intents:
  - `current_weather`
  - `forecast_weather`
  - `thanks`
  - `no_more_help`
 
---

## How it Works

1. User sends query via Dialogflow.
2. Dialogflow hits the webhook (FastAPI endpoint `/webhook`).
3. The webhook processes the intent and returns a response using OpenWeatherMap API.

---

## Installation

1. Clone the repository:
```bash
  git clone https://github.com/MuhammadSheesShoaib/weather_forecast_agent_dialogflow.git
  cd weather_forecast_agent_dialogflow
 ```
2. Create virtual environment and install dependencies:
```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
 ```
3. Run the server:
```bash
  uvicorn main:app --reload
```
## Configuration
Update the API_KEY variable in main.py with your OpenWeatherMap API key.
