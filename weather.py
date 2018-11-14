# WEATHER.PY
# AUTHOR: AARON PENNINGTON
# All functions needed to get the weather information for the user. 

import time
import requests
import json
import math
import sys
from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow


# TO DO
# 1. Restructure weather class. Some of the functions are outdated. Others are obtuse or unclear. 
#    There should be two functions which return the current weather as an int and the forecast as
#    a list, respectively. 
# 2. Remove the command parsing. The gui makes this unnecessary. 
# 3. Remove the time checking. It's now unused because of how the api calls are made. 
# 4. Determine a way to insert the actual weather data into the gui labels. 
# 5. Remove this todo list. :)

class Weather():
    def __init__(self):
        self.module_name = "Weather"
        self.module_desc = "Get the weather for your location."


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

        return res


    # Opens the weather JSON file and returns the temp
    def read_weather(self, res):
        j = json.loads(res.text)
        temperature = j['main']['temp']
        return temperature 


    # Opens weather JSON file and returns the forecast
    def read_forecast(self, res):
        weather = json.loads(res.text)
        t_list = []
        t_dict = dict()
        num = 0

        for day in weather['list']:
            date = day['dt']
            temp = day['main']['temp']

            d = self.convert_date(float(date))
            t = self.convert_temp(temp)

            if num < 7:
                t_list.append(t)
                num += 1
            elif num == 7:
                t_list.append(t)
                self.sort_list(t_list)
                high = t_list[len(t_list) - 1]
                low = t_list[0]
                temps = []

                temps.append(high)
                temps.append(low)
                t_dict[d] = temps

                num = 0
                t_list = []

        return t_dict

    # Converts temperature from Kelvin to Fahrenheit
    def convert_temp(self, temp_kel):
        temp_fah = (temp_kel * 1.8) - 459.67
        temp_fah = math.ceil(temp_fah)
        return int(temp_fah)


    # Converts a Unix Epoch timestamp into human readable format
    def convert_date(self, date):
        new_date = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(date))
        return new_date


    # Bubble Sort Algorithm
    # Source: https://github.com/TheAlgorithms/Python/blob/master/sorts/bubble_sort.py
    def sort_list(self, t_list):
        length = len(t_list)
        for i in range(length-1):
            swapped = False
            for j in range(length-1-i):
                if t_list[j] > t_list[j+1]:
                    swapped = True
                    t_list[j], t_list[j+1] = t_list[j+1], t_list[j]
            if not swapped: break

        return t_list


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
        cd = self.convert_date(time_updated)
        return cd


    def get_current(self):
        current_api_call = self.call_weather("weather")
        current_res = self.make_call(current_api_call, "weather")
        current_temp_kelvin = self.read_weather(current_res)
        current_temp_fahrenheit = self.convert_temp(current_temp_kelvin)
        return current_temp_fahrenheit


    def get_forecast(self):
        forecast_api_call = self.call_weather("forecast")
        forecast_res = self.make_call(forecast_api_call, "forecast")
        forecast_list = self.read_forecast(forecast_res)
        print(str(forecast_list))


    # Compare the time at last API call to the current time.
    def get_weather(self):
        current_api_call = self.call_weather("weather")
        forecast_api_call = self.call_weather("forecast")

        current_res = self.make_call(current_api_call, "weather")
        forecast_res = self.make_call(forecast_api_call, "forecast")

        current_temp_kelvin = self.read_weather(current_res)
        current_temp_fahrenheit = self.convert_temp(current_temp_kelvin)

        forecast_list = self.read_forecast(forecast_res)
        





class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


    def updateLabel(self, cw):
        self.ui.updateLabel(cw)


def main():
    weather = Weather()
    cw = weather.get_current()
    fw = weather.get_forecast()
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.updateLabel(cw)
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()