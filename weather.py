import requests
import pandas as pd
import plotly.express as px

API_KEY ="your API_KEY"

# 📝 Input cities
cities = input("Enter city names separated by commas: ").split(",")

for city in cities:
    city = city.strip()
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # 🛡️ Check if city data is valid
    if data.get("cod") != "200":
        print(f"⚠️ Could not fetch data for {city}: {data.get('message', 'Unknown error')}")
        continue

    weather_list = data["list"]

    # 📊 Collect multiple metrics
    weather_data = {
        "date": [item["dt_txt"] for item in weather_list],
        "temp": [item["main"]["temp"] for item in weather_list],
        "humidity": [item["main"]["humidity"] for item in weather_list],
        "wind": [item["wind"]["speed"] for item in weather_list]
    }

    df = pd.DataFrame(weather_data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    # 📆 Daily averages
    df["day"] = df.index.date
    daily_avg = df.groupby("day").mean()

    # 🚨 Alerts
    if daily_avg["temp"].max() > 40:
        print(f"🔥 Heat alert in {city}! Max temp: {daily_avg['temp'].max():.1f}°C")
    if daily_avg["wind"].max() > 20:
        print(f"💨 Strong winds expected in {city}! Max wind: {daily_avg['wind'].max():.1f} m/s")

    # 📈 Interactive Plotly chart
    fig = px.line(
        daily_avg,
        x=daily_avg.index,
        y=["temp", "humidity", "wind"],
        labels={"value": "Weather Metrics", "variable": "Metric"},
        title=f"{city} - Daily Weather Trends"
    )
    fig.show()



