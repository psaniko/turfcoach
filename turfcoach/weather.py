import os

import click
import requests
import plotext as plt


def openweather_request(path: str, params: dict = dict()) -> dict:
    """Make a request to the OpenWeather API."""

    BASE_PATH = "https://api.openweathermap.org/"
    API_KEY = os.environ.get("OPENWEATHER_API_KEY")
    if not API_KEY:
        raise ValueError(
            "No API key found. Please provide an API key in the environment variable OPENWEATHER_API_KEY."
        )

    # Make request and add API key to params
    r = requests.get(BASE_PATH + path, params={**params, "appid": API_KEY})

    json = r.json()
    if r.status_code != 200:
        raise ValueError(
            f"Request failed with status code {r.status_code} and message {json['message']}."
        )

    return json


def fetch_coordinates(city: str) -> tuple:
    """Fetch coordinates for a given city."""

    result = openweather_request(f"geo/1.0/direct", params={"q": city})
    if not result:
        raise ValueError(f"Could not find coordinates for {city}.")

    # Take the first match on the assumption that it is the most relevant
    first_match = result[0]

    click.echo(
        f"Interpreting '{city}' as {first_match['name']}, {first_match['country']}."
    )
    return first_match["lat"], first_match["lon"]


def fetch_weather(city: str) -> dict:
    """Fetch weather stats for a given city."""

    lat, lon = fetch_coordinates(city)

    result = openweather_request(
        f"data/2.5/weather",
        params={
            "lat": lat,
            "lon": lon,
            "units": "metric",
        },
    )
    if not result:
        raise ValueError(f"Could not find weather stats for {city}.")

    return result  # return the entire response for simplicity


def print_stats(city_data: dict[str, dict]) -> None:
    """Print statistics for a list of cities.

    Args:
        city_data: A dictionary where the keys are user-provided city names and the values are
                   dictionaries containing[weather data](https://openweathermap.org/current#example_JSON).
    """

    # Print city with the highest temperature
    temperatures_by_city = {
        city: data["main"]["temp"] for city, data in city_data.items()
    }
    max_temp = max(temperatures_by_city.values())
    max_temp_city = max(temperatures_by_city, key=temperatures_by_city.get)
    click.echo(f"Highest temperature: {max_temp_city} with {max_temp}°C")

    # Print city with the lowest humidity
    humidities_by_city = {
        city: data["main"]["humidity"] for city, data in city_data.items()
    }
    min_humidity = min(humidities_by_city.values())
    min_humidity_city = min(humidities_by_city, key=humidities_by_city.get)
    click.echo(f"Lowest humidity: {min_humidity_city} with {min_humidity}%")

    # Find most common weather condition
    # There is a shorter way to write the code below. I chose this for clarity.
    weather_freq = {}
    for data in city_data.values():
        weather = data["weather"][0]["main"]
        if weather in weather_freq:
            weather_freq[weather] += 1
        else:
            weather_freq[weather] = 1
    most_common_weather = max(weather_freq, key=weather_freq.get)
    click.echo(f"Most common weather condition: {most_common_weather}")

    # Print histogram of temperatures across cities
    temperatures = [data["main"]["temp"] for data in city_data.values()]

    click.echo("")  # new line
    plt.hist(temperatures, bins=10)
    plt.plot_size(60, 20)
    plt.title("Histogram of temperatures across cities")
    plt.show()


@click.command()
@click.option(
    "-c",
    "--city",
    multiple=True,
    default=["Berlin", "London", "New York"],
    help="Provide a list of cities to fetch weather stats for. If not provided, a default list of cities will be used.",
)
def run_prompt(city):
    cities = city  # rename for clarity

    click.echo("Cities: {}\n".format(", ".join(cities)))

    # Fetch geocoordinates and weather data sequentially
    try:
        city_data = {city: fetch_weather(city) for city in cities}
    except ValueError as e:
        click.echo(f"Error while trying to fetch weather data: {e}")
        return

    click.echo("")  # new line

    print_stats(city_data)


if __name__ == "__main__":
    run_prompt()
