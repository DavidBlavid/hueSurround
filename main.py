import Color_Calculation

from phue import Bridge
from rgbxy import Converter

import requests
import time
import random

# Change these Values to configure the Program
api_key = "7cc413a42a25e77da241b94936228c87"
city_name = "Hamburg"
light_ip = '192.168.178.29'

# Connect to Weather API
base_url = "http://api.openweathermap.org/data/2.5/weather?"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# Set up a RGB to XY Converter
converter = Converter()

# Connect to Light
light = Bridge(light_ip)
light.connect()

# Test if Light can be turned on
light.set_light(1, 'on', True)

if light.get_light(1, 'on'):

    print("[phue] Light has been found!\n")

    while True:

        # Get JSON Weather Data
        response_request = requests.get(complete_url)
        response_json = response_request.json()


        # Get Calculated RGB Color and calculate its XY
        current_data = Color_Calculation.get_color(response_json)
        current_rgb = current_data[0:3]
        current_brightness = current_data[3]

        current_xy = converter.rgb_to_xy(current_rgb[0], current_rgb[1], current_rgb[2])

        # Send Color and Brightness to Lamp

        light.set_light(1, 'xy', current_xy)
        light.set_light(1, 'bri', current_brightness, transitiontime = 5 + random.random() * 5)

        time.sleep(10 + random.random() * 5)


else:

    print("[phue] No Light was found")