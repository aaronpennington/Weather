# WEATHER.PY
# AUTHOR: AARON PENNINGTON
# All functions needed to get the weather information for the user. 

import time
import requests
import json

class Weather():
    #ok, class vars are weird in python. you wanna use self.var, but not self.var, it's self.__class__.var, or something. 
    #I have to work tommorrow. I don't wanna deal with this. 
    #But once i sort out these vars, everything should work
    #Except oh yeah, there are multiple cities in the city list with the same name. So instead of getting city id based
    #on city name, i will have to use latitude and longitude.
    #SO, i have to find a way to use geolocation or something. 
    #I just wanted to get the weather. 
    #jeez
    #JEEZ!
    #come on.

    #good luck.


    def __init__(self):
        self.module_name = "Weather"
        self.module_desc = "Get the weather for your location."


    # Searches a LARGE list of cities to get the id of the city the user is in
    def get_city_id(self):
        loc = input("Location: ")
        city_id = ''
        with open("city_list.json", "r", encoding = 'utf-8') as city_file:
            city_list = json.load(city_file)
            for city in city_list:
                if city['name'] == loc:
                    city_id = str(city['id'])
        return city_id


    # Reads an OpenWeatherMap API key from a local text file. 
    def get_api_key(self):
        try:
            with open('api_key.txt', 'r') as api_key_file:
                api_key = api_key_file.read()
            return api_key
        except IOError:
            print ("Error: No API key found.")


    # Calls the weather website and downloads a JSON file
    def make_call(self):
        city_id = self.get_city_id()
        print("City ID: " + str(city_id))
        api_key = self.get_api_key()

        api_call = "http://api.openweathermap.org/data/2.5/weather?id=" + str(city_id) + \
                       "&APPID=" + str(api_key)

        res = requests.get(api_call)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % exc)

        with open('weather.json', 'w') as weather_file:
                weather_file.write(res.text)
                

    # Opens the weather JSON file and returns the temp
    def read_weather(self):
        with open('weather.json', 'r') as weather_file:
            weather = json.load(weather_file)
            temp_kel = float(weather['main']['temp'])
        return temp_kel


    # Converts temperature from Kelvin to Fahrenheit
    def convert_temp(self):
        temp_kel = self.read_weather()
        temp_fah = (temp_kel * 1.8) - 459.67
        return temp_fah


    # Updates the time at last API call. Sets the value to the current time.
    def update_time(self):
            up_time = open('time.txt', 'w')
            new_time = time.time()
            up_time.write(str(new_time))
            up_time.close()


    # Compare the time at last API call to the current time. If less than 10 min have passed, use last
    # weather info. 
    def check_time(self):
        file_time = open('time.txt', 'r')
        time_last_call = float(file_time.read())
        time_current = time.time()
        file_time.close()

        if time_current - time_last_call < 660:
            temp_fah = self.convert_temp()
            print("Temperature: " + "%.2f" % round(temp_fah, 2))
            print("Less than 10 minutes have passed.")

        elif time_current - time_last_call >= 660:
            self.make_call()
            temp_fah = self.convert_temp()
            print("Temperature: " + "%.2f" % round(temp_fah, 2))

            self.update_time()

            print("More than 10 minutes have passed.")
        else:
            print("Error getting the time.")


weather = Weather()
weather.check_time()