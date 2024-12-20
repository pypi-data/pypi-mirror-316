import argparse
from .weather import get_weather


def main():
    parser = argparse.ArgumentParser(
        description="Weather CLI - Get the current weather for a city."
    )
    parser.add_argument("city", help="City name for which.")
    args = parser.parse_args()

    try:
        weather = get_weather(args.city)
        print(
            f"Current weather in {args.city}: "
            f"{weather['temperature']}°C, {weather['description']}"
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
