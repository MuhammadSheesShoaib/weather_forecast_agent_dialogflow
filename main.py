from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
from datetime import datetime, timedelta

app = FastAPI()

API_KEY = "OPEN_WEATHER_API"  # openweather api key

@app.post("/webhook")
async def webhook(request: Request):
    req = await request.json()
    intent_name = req["queryResult"]["intent"]["displayName"]
    params = req["queryResult"]["parameters"]

    city = params.get("geo-city")
    if not city:
        return JSONResponse(content={"fulfillmentText": "Please tell me which city you're asking about."})

    if intent_name == "current_weather":
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()
        try:
            desc = res["weather"][0]["description"]
            temp = res["main"]["temp"]
            response_text = f"The current weather in {city} is {desc} with a temperature of {temp}°C."
        except:
            response_text = f"Sorry, I couldn't find the weather for {city}."

    elif intent_name == "forecast_weather":
        try:
            start_str = params["date-period"]["startDate"]
            end_str = params["date-period"]["endDate"]
            start_date = datetime.fromisoformat(start_str)
            end_date = datetime.fromisoformat(end_str)
        except (KeyError, TypeError, ValueError):
            response_text = "Sorry, I couldn't understand the date range you mentioned."
            return JSONResponse(content={"fulfillmentText": response_text})

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        if "list" not in res:
            response_text = f"Sorry, I couldn't retrieve forecast data for {city}."
            return JSONResponse(content={"fulfillmentText": response_text})

        forecasts = res["list"]
        daily_summary = {}

        for entry in forecasts:
            dt = datetime.utcfromtimestamp(entry["dt"])
            if start_date.date() <= dt.date() <= end_date.date():
                date_str = dt.strftime("%Y-%m-%d")
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"]

                if date_str not in daily_summary:
                    daily_summary[date_str] = {
                        "temps": [],
                        "descs": []
                    }

                daily_summary[date_str]["temps"].append(temp)
                daily_summary[date_str]["descs"].append(desc)

        if not daily_summary:
            response_text = f"Sorry, no forecast data was found between those dates for {city}."
        else:
            sorted_dates = sorted(daily_summary.keys())[:8]
            response_text = f"Here's the weather forecast for {city} from {sorted_dates[0]} to {sorted_dates[-1]}:"
            for date_str in sorted_dates:
                avg_temp = sum(daily_summary[date_str]["temps"]) / len(daily_summary[date_str]["temps"])
                desc = max(set(daily_summary[date_str]["descs"]), key=daily_summary[date_str]["descs"].count)
                response_text += f"\n• {date_str}: {desc}, {avg_temp:.1f}°C"

    else:
        response_text = "Sorry, I couldn't understand your request."

    return JSONResponse(content={"fulfillmentText": response_text})
