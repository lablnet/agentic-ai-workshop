"""Current weather from Open-Meteo."""

import json
import logging

import requests


def get_weather(location: str) -> str:
    """Get current temperature and wind speed for a city, for example Islamabad."""
    logging.info("TOOL | get_weather | %s", location)
    try:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1}, timeout=15,
        )
        response.raise_for_status()
        places = response.json().get("results", [])
        if not places:
            return f"No location found for {location}."
        place = places[0]
        response = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": place["latitude"], "longitude": place["longitude"],
            "current": "temperature_2m,wind_speed_10m", "timezone": "auto",
        }, timeout=15)
        response.raise_for_status()
        weather = response.json()
        return json.dumps({"location": place["name"], "country": place.get("country"),
                           "current": weather["current"], "units": weather["current_units"]})
    except (requests.RequestException, ValueError, KeyError) as error:
        return f"Weather API unavailable: {error}"
