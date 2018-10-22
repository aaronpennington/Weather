# WEATHER.PY
# AUTHOR: AARON PENNINGTON
# All functions needed to get the weather information for the user. 

import time
import requests
import json

class Weather():
    def __init__(self):
        self.module_name = "Weather"
        self.module_desc = "Get the weather for your location."

    # Requests input from user
    def get_command(self):
        print("Please input a command.")
        command = input("> ")
        return command

    # Uses user IP to get a json file containing the coordinates of their location. 
    def get_coords(self):
        url = "http://ipinfo.io/json"

        try:
            req = requests.get(url)
        except:
            print("Unable to connect to Internet.")
            input("Press ENTER to exit.")

        with open("ip_info.json", "w+") as ip_file:
            ip_file.write(req.text)
        with open("ip_info.json", "r+") as ip_file:
            location = json.load(ip_file)
            coords = location["loc"]

        return coords


    # Reads an OpenWeatherMap API key from a local text file. 
    def get_api_key(self):
        try:
            with open('api_key.txt', 'r') as api_key_file:
                api_key = api_key_file.read()
            return api_key
        except IOError:
            print ("Error: No API key found.")


    # Creates the url for the API call depending on the user command
    def call_weather(self, type):
        coords = self.get_coords()
        lat, lon = coords.split(',')

        api_key = self.get_api_key()

        api_call = "http://api.openweathermap.org/data/2.5/" + type + "?lat=" + lat + "&lon=" + lon + \
                   "&APPID=" + str(api_key)

        return api_call


    # Requests the weather json from openweathermap.org
    def make_call(self, api_call, type):
        res = requests.get(api_call)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % exc)

        with open('weather.json', 'r') as wf:
            w_data = wf.read()
            w_json = json.loads(w_data)

            if (type == "weather"):
                w_json['current'] = res.text
            elif (type == "hourly"):
                w_json['hourly'] = res.text

        with open('weather.json', 'w+') as weather_file:
            weather_file.write(json.dumps(w_json, indent = 4))


    # Opens the weather JSON file and returns the temp
    def read_weather(self):
        with open('weather.json', 'r') as wf:
            w_json = json.load(wf)
        
            temp_kel = float(w_json['current']['main']['temp'])
        return temp_kel


    # Opens weather JSON file and returns the forecast
    def read_forecast(self):
        with open('weather.json', 'r+') as weather_file:
            weather = json.load(weather_file)
        forecast = weather['hourly']['list']
        for forecast in weather:
            date = forecast['dt']
            temp = forecast['main']['temp']
            
            d = convert_date(date)
            t = convert_temp(temp)

            print("Date: " + d + "\nTemperature: " + t)
            print("")


    # Converts temperature from Kelvin to Fahrenheit
    def convert_temp(self, temp_kel):
        temp_kel = self.read_weather()
        temp_fah = (temp_kel * 1.8) - 459.67
        return temp_fah


    # Converts a Unix Epoch timestamp into human readable format
    def convert_date(self, date):
        new_date = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(date))
        return new_date


    # Updates the time at last API call. Sets the value to the current time.
    def update_time(self):
        up_time = open('time.txt', 'w+')
        new_time = time.time()
        up_time.write(str(new_time))
        up_time.close()


    # Reads the unix epoch time from time.txt file, and converts it to a readable format
    def get_time(self):
        with open("time.txt", "r+") as t_file:
            time_updated = float(t_file.read())
        return convert_date(time_updated)


    # Compare the time at last API call to the current time. If less than 10 min have passed, use last
    # weather info. 
    def check_time(self, type):

        file_time = open('time.txt', 'r+')
        time_last_call = float(file_time.read())
        time_current = time.time()
        file_time.close()

        if time_current - time_last_call < 660:
            temp_kel = self.read_weather()
            temp_fah = self.convert_temp(temp_kel)
            print("Temperature: " + "%.2f" % round(temp_fah, 2))

        elif time_current - time_last_call >= 660:
            api_call = self.call_weather(type)
            self.make_call(api_call, type)

            temp_kel = self.read_weather()
            temp_fah = self.convert_temp(temp_kel)
            print("Temperature: " + "%.2f" % round(temp_fah, 2))

            self.update_time()

        else:
            print("Error getting the time.")

        print("Last updated: " + self.get_time())


    # If/Else statements for various user commands (current, hourly, or daily forecast)
    def parse_command(self, command):
        if (command == "weather"):
            t = "weather"
        elif (command == "hourly"):
            t = "forecast"
        else:
            print("Command unable to be parsed.")
            self.get_command()

        self.check_time(t)


weather = Weather()
weather.parse_command(weather.get_command())

input("Press ENTER to exit.")