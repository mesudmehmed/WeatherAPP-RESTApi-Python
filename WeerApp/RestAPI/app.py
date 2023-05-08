# Importing necessary libraries
from flask import Flask, jsonify, render_template, request
from weer_model import WeerModel

# Creating a Flask app instance
app = Flask(__name__)

# Initializing a WeerModel object with configuration file 'settings.ini'
weer_model = WeerModel('settings.ini')

# Defining a route for getting forecast data
@app.route('/forecast', methods=['GET'])
def get_forecast():
    # Getting forecast data from the WeerModel object
    output = weer_model.get_forecast()
    # Returning forecast data in JSON format
    return jsonify(output)

# Defining a route for displaying and modifying settings
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Getting current settings values from the WeerModel object
    max_temp = weer_model.get_setting('max_temp')
    min_temp = weer_model.get_setting('min_temp')
    max_wind_speed = weer_model.get_setting('max_wind_speed')
    max_rain_chance = weer_model.get_setting('max_rain_chance')
    max_snow_chance = weer_model.get_setting('max_snow_chance')
    weather_location = weer_model.config.get('Settings', 'weather_location')
    weather_time = weer_model.config.get('Settings', 'weather_time')

    # Handling POST requests for updating settings
    if request.method == 'POST':
        # Updating settings with values from the POST request
        max_temp = request.form['max_temp']
        min_temp = request.form['min_temp']
        max_wind_speed = request.form['max_wind_speed']
        max_rain_chance = request.form['max_rain_chance']
        max_snow_chance = request.form['max_snow_chance']
        weather_location = request.form['weather_location']
        weather_time = request.form['weather_time']

        # Updating configuration file with new settings values
        weer_model.config.set('Settings', 'max_temp', str(max_temp))
        weer_model.config.set('Settings', 'min_temp', str(min_temp))
        weer_model.config.set('Settings', 'max_wind_speed', str(max_wind_speed))
        weer_model.config.set('Settings', 'max_rain_chance', str(max_rain_chance))
        weer_model.config.set('Settings', 'max_snow_chance', str(max_snow_chance))
        weer_model.config.set('Settings', 'weather_location', weather_location)
        weer_model.config.set('Settings', 'weather_time', weather_time)
        # Writing updated configuration file to disk
        with open('settings.ini', 'w') as configfile:
            weer_model.config.write(configfile)

    # Rendering the settings page with current settings values
    return render_template('settings.html', max_temp=max_temp, min_temp=min_temp, max_wind_speed=max_wind_speed, max_rain_chance=max_rain_chance, max_snow_chance=max_snow_chance, weather_location=weather_location, weather_time=weather_time)


# Running the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)