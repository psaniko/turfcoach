# Weather Stats (for Turfcoach)

Minimalistic Python script to prompt a shell user for cities and print weather stats for them.

## Requirements

### An API key from openweathermap.org

1. [Sign up](https://home.openweathermap.org/users/sign_up) for an OpenWeather account
1. Confirm your email address
1. Go to [API keys](https://home.openweathermap.org/api_keys) and copy the default key (or create a custom one)

## Installation

1. Clone this repository

   ```sh
   git clone {paste-url}
   ```

1. Add your API key as an environment variable

   ```sh
   export OPENWEATHER_API_SECRET={YOUR API KEY}
   ```

1. Install dependencies

   ```sh
   poetry install
   ```

## Usage

1. Run the script
   ```sh
   poetry run python turfcoach/weather.py --city "San Francisco" --city Berlin --city Dublin --city Lima
   ```


## Design Considerations

1. Minimal filestructure: One could argue to extract the code in `weather.py` into all kinds of files. With the scope as it is, I believe the simplicity of one file outweighs the benefits of a more nuanced file structure.

1. Poetry: I went for Poetry over `pyenv`, `venv`, `virtualwrapper`, etc simply because I hadn't tried it yet and was curious.

1. Async: For a larger project of this kind I would strongly consider async or some coroutine library, not only to parallelize fetch requests for muliple cities. As it is, this seemed the simplest way to the target.

1. Other bells and whistles: I considered adding custom exceptions, tests, a license, `.gitignore`, and a proper frontend but, again, decided for the MVP version.


### Additional libraries

- `click` for a minimal command-line interface
- `requests` for convenient API calls (instead of `urllib.request`)
- `plotext` for printing a histogram to the command line

While a large-scale application might benefit from `pandas`, I deliberately went for dictionaries for the sake of simplicity.
