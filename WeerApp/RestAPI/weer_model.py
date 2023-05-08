import requests # import the requests library to make HTTP requests
from datetime import datetime, timedelta # import datetime module to work with dates and times
import configparser # import configparser module to work with configuration files

# Create a class to handle weather forecasting using OpenWeatherMap API
class WeerModel:
    def __init__(self, settings_file):
        # Store the name of the settings file for later reference
        self.settings_file_name = settings_file
        # Create a ConfigParser object to read the settings file
        self.config = configparser.ConfigParser()
        self.config.read(settings_file)
        # Set the default category to "Settings"
        self.default_category = "Settings"
        # Define the URL for the OpenWeatherMap API, including the API key and units
        self.url = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid=bb7a179221da8c9dc578db614841ef9d&units=metric'

    # Helper method to retrieve a setting from the settings file
    def get_setting(self, setting_name):
        return int(self.config.get(self.default_category, setting_name))

    # Method to get the weather forecast for a given location and time
    def get_forecast(self, weather_location=None, weather_time=None):
        # Use default location and time settings if none are provided
        if not weather_location:
            weather_location = self.config.get(self.default_category, 'weather_location')
        if not weather_time:
            weather_time = self.config.get(self.default_category, 'weather_time')
        
        # Retrieve max/min temperature, max wind speed, max rain chance, and max snow chance from settings file
        max_temp = self.get_setting('max_temp')
        min_temp = self.get_setting('min_temp')
        max_wind_speed = float(self.get_setting('max_wind_speed'))
        max_rain_chance = self.get_setting('max_rain_chance')
        max_snow_chance = self.get_setting('max_snow_chance')

        # Define the forecast date range as the next four days
        today = datetime.today().date()
        dates = [today + timedelta(days=i) for i in range(4)]

        # Get the weather forecast data from the OpenWeatherMap API
        response = requests.get(self.url.format(weather_location)).json()
        forecasts = response['list']

        # Initialize an empty list to store the bikeability forecast for each date
        forecast = []

        # Convert the specified weather time to a datetime object for comparison with forecast data
        now = datetime.now()
        weather_time = datetime(now.year, now.month, now.day, int(weather_time.split(':')[0]),
                                int(weather_time.split(':')[1]))

        # Iterate over each forecast date and each forecast item to determine bikeability
        for date in dates:
            for item in forecasts:
                dt = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
                # Skip items that don't match the current date
                if dt.date() != date:
                    continue
                # Retrieve temperature, wind speed, and precipitation chance data from forecast item
                temp = item['main']['temp']
                wind_speed = item['wind']['speed']
                rain_chance = item['pop']
                # Check for snow data and set snow chance accordingly
                snow_chance = item['snow']['1h'] if 'snow' in item and '1h' in item['snow'] else 0
                # Determine if the weather is suitable for biking based on the max/min temperature, max wind speed, max rain chance, and max snow chance settings
                if wind_speed > max_wind_speed or rain_chance > max_rain_chance or snow_chance > max_snow_chance or temp < min_temp or temp > max_temp:
                     # check if the weather conditions are suitable for biking based on the configuration settings
                    bike_weather = False # if any of the conditions are not suitable, set bike_weather to False
                else:
                    bike_weather = True # if all the conditions are suitable, set bike_weather to True
                forecast.append({'date': date.strftime('%m-%d-%Y'), 'bike_okay': bike_weather})  # add the date and the bike weather condition to the forecast list
                break # break out of the loop once the weather forecast for the current date has been checked

        output = {'location': weather_location, 'departure': weather_time.strftime('%H:%M'), 'okay_to_bike': forecast[:3]}
        # create a dictionary containing the weather location, departure time, and the forecast for the next 3 days
        return output # return the weather forecast dictionary