import time as tm

from datetime import *
from Valuehandler import Valuehandler

# Length of Times in Seconds
UNIX_DAY = 86400
UNIX_HOUR = 3600

# Handles the values from the txt files in colorvalues
vhandler = Valuehandler()

# Instantiate Color and Brightness Variables
current_r = 255
current_g = 255
current_b = 255
current_brightness = 255

def get_color(data):

    # Time Data
    # Every Timestamp is a UNIX Timestamp
    time_current = tm.time()                # Current Time
    time_sunrise = data["sys"]["sunrise"]   # Time of Sunrise
    time_sunset = data["sys"]["sunset"]     # Time of Sunset

    # Get UNIX Timestamps of last and next Midnight (0:00 AM)
    time_midnight_prev = int(tm.mktime(datetime.combine(datetime.today(), time.min).timetuple()))
    time_midnight_next = int(tm.mktime(datetime.combine(datetime.today() + timedelta(1), time.min).timetuple()))

    # Get Solar Noon and Solar Midnight based on Sunset and Sunrise
    time_sl_noon = int(((time_sunset + time_sunrise) / 2))
    time_sl_midnight_prev = int(time_sl_noon - UNIX_DAY / 2)
    time_sl_midnight_next = time_sl_midnight_prev + UNIX_DAY

    # print("\nCURRENT", time_current)

    # print("\nP SL MN", time_sl_midnight_prev)
    # print("PREV MN", time_midnight_prev)
    # print("SUNRISE", time_sunrise)
    # print("SL NOON", time_sl_noon)
    # print("SUNSET ", time_sunset)
    # print("NEXT MN", time_midnight_next)
    # print("N SL MN", time_sl_midnight_next , "\n")

    # Weather Data
    # Weather Groups: https://openweathermap.org/weather-conditions
    weather_id = data["weather"][0]["id"]  # Weather ID
    weather_main = data["weather"][0]["main"]  # Main Weather Group
    weather_description = data["weather"][0]["description"]  # Weather Descriptor
    weather_cloudiness = data["clouds"]["all"]  # Cloudiness in %

    # Wind Data
    wind_speed = data["wind"]["speed"]  # Wind speed in m/s

    # time_percent keeps track of how much Time between the Keyframes has passed (0.0 - 1.0)
    # Used for interpolating the Color Values
    time_percent = 0.1

    # Determine between which Time Keyframes we are

    # Previous Solar Midnight -> Sunrise
    if time_sl_midnight_prev < time_current < time_sunrise - UNIX_HOUR:

        print("{Currently between Previous Solar Midnight and Sunrise}")

        # Calculate time_percent
        time_percent = (time_current - time_sl_midnight_prev) / ((time_sunrise - UNIX_HOUR) - time_sl_midnight_prev)

        # The two colors between which we interpolate
        color_first = [0, 13, 37]
        color_second = [13, 21, 42]


    # In Sunrise
    # Sunrise duration: 2 Hours = 7.200 Seconds
    elif time_sunrise - UNIX_HOUR < time_current < time_sunrise + UNIX_HOUR:

        print("{Currently in Sunrise}")

        # Calculate time_percent
        time_percent = (time_current - time_sunrise - UNIX_HOUR) / (UNIX_HOUR * 2)

        # Get Color Values
        # => 566 Rows
        sunrise_position = int(566 * time_percent)

        # We do not need to interpolate if we get the values directly
        color_first = vhandler.get_sunrise_value(sunrise_position)
        color_second = vhandler.get_sunrise_value(sunrise_position)



    # Sunrise -> Solar Noon
    elif time_sunrise + UNIX_HOUR < time_current < time_sl_noon:

        print("{Currently between Sunrise and Noon}")

        # Calculate time_percent
        time_percent = (time_current - (time_sunrise + UNIX_HOUR)) / (time_sl_noon - (time_sunrise + UNIX_HOUR))

        # The two colors between which we interpolate
        color_first = [36, 120, 234]
        color_second = [135, 212, 255]


    # Solar Noon -> Sunset
    elif time_sl_noon < time_current < time_sunset - UNIX_HOUR:

        print("{Currently between Noon and Sunset}")

        # Calculate time_percent
        time_percent = (time_current - time_sl_noon) / ((time_sunset - UNIX_HOUR) - time_sl_noon)

        # The two colors between which we interpolate
        color_first = [135, 212, 255]
        color_second = [36, 120, 234]


    # In Sunset
    # Sunset duration: 2 Hours = 7.200 Seconds
    elif time_sunset - UNIX_HOUR < time_current < time_sunset + UNIX_HOUR:

        print("{Currently in Sunset}")

        # Calculate time_percent
        time_percent = (time_current - (time_sunset - UNIX_HOUR)) / (UNIX_HOUR * 2)

        # Get Color Values
        # => 566 Rows
        sunset_position = int(566 * time_percent)

        # We do not need to interpolate if we get the values directly
        color_first = vhandler.get_sunset_value(sunset_position)
        color_second = vhandler.get_sunset_value(sunset_position)

    # Sunset -> Next Solar Midnight
    elif time_sunset + UNIX_HOUR < time_current < time_sl_midnight_next:

        print("{Currently between Sunset and Next Solar Midnight}")

        # Calculate time_percent
        time_percent = (time_current - (time_sunset + UNIX_HOUR)) / (time_sl_midnight_next - (time_sunset + UNIX_HOUR))

        # The two colors between which we interpolate
        color_first = [13, 21, 42]
        color_second = [0, 13, 37]


    # Anything else (Should never happen!)
    else:

        # Display full white
        time_percent = 1.
        color_first = [255, 255, 255]
        color_second = [255, 255, 255]

    # Interpolate between the colors based on time_percent
    color_interp = [255, 255, 255]
    color_interp[0] = (int(color_first[0]) * (1 - time_percent)) + (int(color_second[0]) * time_percent)
    color_interp[1] = (int(color_first[1]) * (1 - time_percent)) + (int(color_second[1]) * time_percent)
    color_interp[2] = (int(color_first[2]) * (1 - time_percent)) + (int(color_second[2]) * time_percent)

    # Clamp RGB Values between 0 - 255
    current_r = min(255, color_interp[0])
    current_g = min(255, color_interp[1])
    current_b = min(255, color_interp[2])

    current_r = max(0, current_r)
    current_g = max(0, current_g)
    current_b = max(0, current_b)

    print("PERCENT OF TIME KEYFRAME COMPLETE: " + str(round(time_percent, 4) * 100) + "%\n")
    print("RGB", current_r, current_g, current_b)
    print('\n###\n')

    return [current_r, current_g, current_b, current_brightness]
