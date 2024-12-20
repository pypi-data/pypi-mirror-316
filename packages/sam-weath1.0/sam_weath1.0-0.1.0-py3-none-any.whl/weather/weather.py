import requests

def get_weather(city):
    from .logger import logger  # Import logger here to avoid circular import

    API_URL = "http://api.weatherstack.com/current"
    API_KEY = "a47cc985fd4feb7fe0afe76cdcf9e99e"  # Replace with your actual API key

    if not API_KEY:
        logger.error("API key is missing. Please set the API_KEY environment variable.")
        raise Exception("API key is missing. Set the API_KEY environment variable.")

    params = {
        "access_key": API_KEY,
        "query": city,
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()  # Parse the response as JSON

        logger.debug(f"API Response: {data}")

        if "current" not in data:
            logger.error(f"Unexpected API response format: {data}")
            raise Exception("Unexpected API response format.")

        current_weather = data["current"]
        return {
            "temperature": current_weather["temperature"],
            "description": ", ".join(current_weather["weather_descriptions"])
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise Exception("Failed to fetch weather data")
