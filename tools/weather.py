"""Current weather from Open-Meteo."""

import json
import logging

import requests


def get_weather(location: str) -> str:
    """Get current temperature and wind speed for a city, for example Islamabad."""
    logging.info("TOOL | get_weather | %s", location)
    try:
        # Call the Open-Meteo API
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1}, timeout=15,
        )
        # Raise an error if the request is not successful
        response.raise_for_status()
        # Get the places from the response
        places = response.json().get("results", [])
        # If no places are found, return an error
        if not places:
            return f"No location found for {location}."
        # Get the first place
        place = places[0]
        # Call the Open-Meteo API
        response = requests.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": place["latitude"], "longitude": place["longitude"],
            "current": "temperature_2m,wind_speed_10m", "timezone": "auto",
        }, timeout=15)
        # Raise an error if the request is not successful
        response.raise_for_status()
        # Get the weather from the response
        weather = response.json()
        # Return the weather
        return json.dumps({"location": place["name"], "country": place.get("country"),
                           "current": weather["current"], "units": weather["current_units"]})
    except (requests.RequestException, ValueError, KeyError) as error:
        return f"Weather API unavailable: {error}"
