from datetime import timedelta, datetime
from meteostat import Hourly, Daily

# Nearest weather station: Birmingham Airport (ID: 72228)
WEATHER_STATION = '72228'
# Coordinates for UAB Hill Center: 33.501660, -86.807336

# Converts temperature from fahrenheit to celcius.
def convertFahrenheitToCelcius(temperature):
    return (temperature * 1.8) + 32

# Returns the temperature (F) at the top of the hour of 'datetime'.
def getHourlyTemperature(datetime):
    start = datetime
    end = datetime + timedelta(hours=1) # Add 1 hour to entered time.
    
    # Fetch data from weather station at the next top of hour for entered time.
    # (i.e., 12:33 shows 1:00, 5:01 shows 6:00)
    data = Hourly(WEATHER_STATION, start, end)
    data = data.fetch()

    # Get temperature (celcius) from fetched weather data.
    temperature_C = data['temp'].values[0]

    # Convert temperature from celcius to fahrenheit.
    temperature_F = convertFahrenheitToCelcius(temperature_C)
    return temperature_F

# Returns the average temperature (F) for the following date of 'datetime'.
def getDailyTemperature(datetime):
    start = datetime
    end = datetime + timedelta(days=1) # Add 1 day to entered time.
    
    # Fetch data from weather station for following day of entered time.
    # (i.e., 10/20/2022 shows 10/21/2022)
    data = Daily(WEATHER_STATION, start, end)
    data = data.fetch()

    # Get temperature (celcius) from fetched weather data.
    temperature_C = data['tavg'].values[0]

    # Convert temperature from celcius to fahrenheit.
    temperature_F = convertFahrenheitToCelcius(temperature_C)
    return temperature_F