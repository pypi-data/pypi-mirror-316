import requests, pprint

class Weather:
    """
    Creates a weather object getting an API key as input
    and either a city name or latitude and longitude coordinates.

    Package use example:
    # Create a weather object using a city name
    # The API key below is not guaranteed to work
    # Get your own API key on https://openweathermap.org

    >>> weather = Weather(apikey="94cc097e17d4d0f573b3c34754a1fecc", city="Beirut")

    # Adding longitude and latitude coordinates
    >>> weather = Weather(apikey="94cc097e17d4d0f573b3c34754a1fecc", lat=41.4, lon=-4.1)

    # Get complete weather data for the next 12hr
    >>> weather.next_12hr()

    # Simplified data for the next 12hr
    >>> weather.next_12hr_simplified()

    # Get weather data for the next 5 days
    >>> weather.next_5days()

    # Sample url to get weather condition icon:
    https://openweathermap.org/img/wn/10d@2x.png
    """

    def __init__(self, apikey, city=None, lat=None, lon=None, units="metric"):
        if not apikey:
            raise ValueError("API key is required")

        if units not in ['metric', 'imperial']:
            raise ValueError("Invalid units. Please use 'metric' or 'imperial'.")

        self.url = self._build_url(apikey, city, lat, lon, units)
        self.data = self._fetch_weather_data()

    def _build_url(self, apikey, city, lat, lon, units):
        """Builds the API URL based on provided parameters."""
        if city:
            return f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units={units}"
        elif lat and lon:
            return f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units={units}"
        else:
            raise TypeError("Provide either a city or lat and lon arguments")

    def _fetch_weather_data(self):
        """Fetch weather data from the OpenWeather API."""
        r = requests.get(self.url)
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError(f"API request failed with status code {r.status_code}: {r.text}")
    def next_12hr(self):
        """
        Retrieves detailed weather data for the next 12 hours.

        Returns:
            list: A list of dictionaries containing detailed weather forecasts.
        """
        return self.data['list'][:4]

    def next_12hr_simplified(self):
        """
        Retrieves simplified weather data for the next 12 hours.

        Returns:
            list: A list of tuples containing (datetime, temperature, weather condition).
        """
        forecast = []
        for d in self.data['list'][:4]:
            forecast.append((d['dt_txt'], d['main']['temp'], d['weather'][0]['description'],
                             d['weather'][0]['icon']))
        return forecast

    def next_5days(self):
        """
        Retrieves weather data grouped by day for the next 5 days.

        Returns:
            dict: A dictionary where keys are dates and values are lists of tuples
                  (time, temperature, weather condition) for that day.
        """
        forecast = {}
        for d in self.data.get('list', []):
            date = d['dt_txt'].split()[0]
            time = d['dt_txt'].split()[1]
            forecast.setdefault(date, []).append((time, d['main']['temp'], d['weather'][0]['description'],
                                                         d['weather'][0]['icon']))
        return forecast





