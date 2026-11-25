
import requests
import re


# --------------------------------------------------
# LOCATION SEARCH
# --------------------------------------------------

def get_coordinates(location_name):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location_name,
        "count": 5,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        locations = data.get("results", [])

        if not locations:
            return {
                "error": f"Location not found: {location_name}"
            }

        # Prefer a matching Indian location
        selected_location = None

        for location in locations:
            if location.get("country_code") == "IN":
                selected_location = location
                break

        if selected_location is None:
            selected_location = locations[0]

        return {
            "latitude": selected_location["latitude"],
            "longitude": selected_location["longitude"],
            "location": selected_location["name"],
            "state": selected_location.get("admin1", ""),
            "country": selected_location.get("country", "")
        }

    except requests.exceptions.RequestException as error:
        return {
            "error": f"Location search failed: {error}"
        }

    except (KeyError, ValueError) as error:
        return {
            "error": f"Unable to process location data: {error}"
        }


# --------------------------------------------------
# EXTRACT LOCATION FROM QUESTION
# --------------------------------------------------

def extract_weather_location(query):

    if not query or not query.strip():
        return "Pune"

    query = query.strip()

    patterns = [
        r"\bin\s+([a-zA-Z\s]+?)(?:\s+today|\s+now|\?|$)",
        r"\bat\s+([a-zA-Z\s]+?)(?:\s+today|\s+now|\?|$)",
        r"\bfor\s+([a-zA-Z\s]+?)(?:\s+today|\s+now|\?|$)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            query,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return "Pune"


# --------------------------------------------------
# GET WEATHER
# --------------------------------------------------

def get_weather(location_name="Pune"):

    # Step 1: Get location coordinates
    location_data = get_coordinates(location_name)

    if "error" in location_data:
        return location_data

    latitude = location_data["latitude"]
    longitude = location_data["longitude"]

    # Step 2: Fetch current weather
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "rain",
            "wind_speed_10m",
            "weather_code"
        ],
        "timezone": "Asia/Kolkata"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        current = data["current"]

        # API observation timestamp
        data_timestamp = current["time"]

        # Step 3: Return weather and source information
        return {

            # Location information
            "location": location_data["location"],
            "state": location_data["state"],
            "country": location_data["country"],

            # Weather information
            "date_time": data_timestamp,
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "precipitation": current["precipitation"],
            "rain": current["rain"],
            "wind_speed": current["wind_speed_10m"],
            "weather_code": current["weather_code"],

            # Source and citation information
            "source": "Open-Meteo Weather API",
            "source_url": "https://open-meteo.com/",
            "data_type": "Current weather",
            "data_as_of": data_timestamp,
            "timezone": data.get("timezone", "Asia/Kolkata")

        }

    except requests.exceptions.RequestException as error:

        return {
            "error": f"Weather API connection failed: {error}"
        }

    except (KeyError, ValueError, TypeError) as error:

        return {
            "error": f"Unable to process weather data: {error}"
        }


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    for city in ["Pune", "Nashik", "Mumbai"]:

        weather = get_weather(city)

        print("\n===== WEATHER REPORT =====")

        if "error" in weather:

            print(weather["error"])

        else:

            print("Location:", weather["location"])
            print("State:", weather["state"])
            print("Country:", weather["country"])

            print("Date & Time:", weather["date_time"])

            print("Temperature:", weather["temperature"], "°C")
            print("Humidity:", weather["humidity"], "%")
            print("Precipitation:", weather["precipitation"], "mm")
            print("Rain:", weather["rain"], "mm")
            print("Wind Speed:", weather["wind_speed"], "km/h")
            print("Weather Code:", weather["weather_code"])

            print("\n----- SOURCE INFORMATION -----")

            print("Data Type:", weather["data_type"])
            print("Data As Of:", weather["data_as_of"])
            print("Timezone:", weather["timezone"])
            print("Source:", weather["source"])
            print("Source URL:", weather["source_url"])
