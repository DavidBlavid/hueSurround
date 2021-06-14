# A handler for the sunrise_values.txt and sunset_values.txt files in colorvalues

class Valuehandler:
    sunrise_values = []
    sunset_values = []

    def __init__(self):

        with open('colorvalues/sunrise_values.txt', 'r') as file:
            data = file.read().split('\n')

            for d in data:
                lightvalue_current = d.split(',')
                self.sunrise_values.append(lightvalue_current)

        with open('colorvalues/sunset_values.txt', 'r') as file:
            data = file.read().split('\n')

            for d in data:
                lightvalue_current = d.split(',')
                self.sunset_values.append(lightvalue_current)

    # Returns a value from sunrise.txt at specific indec
    def get_sunrise_value(self, index):

        return self.sunrise_values[index]

    # Returns a value from sunset.txt at specific indec
    def get_sunset_value(self, index):

        return self.sunset_values[index]
