# -*- coding: utf-8 -*-

# WEATHER.PY
# AUTHOR: AARON PENNINGTON
# A nifty program that displays the current temperature and a five day weather
# forecast!
# https://www.github.com/aaronpennington/Weather

import time
import requests
import json
import math
import sys
from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow
from pathlib import Path

path = Path(__file__).parent.absolute()


class Weather():
    def __init__(self):
        self.module_name = "Weather"
        self.module_desc = "Get the weather for your location."

    # Uses user IP to get a json file containing the coordinates of their
    # location.
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
            with open(str(path) + '/api_key.txt', 'r') as api_key_file:
                api_key = api_key_file.read()
            return api_key
        except IOError:
            print("Error: No API key found.")

    # Creates the url for the API call depending on the user command

    def call_weather(self, type):
        coords = self.get_coords()
        lat, lon = coords.split(',')

        api_key = self.get_api_key()

        api_call = "http://api.openweathermap.org/data/2.5/" + type + \
            "?lat=" + lat + "&lon=" + lon + \
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
        city = j['name']
        return temperature, city

    # Opens weather JSON file and returns the forecast

    def read_forecast(self, res):
        weather = json.loads(res.text)
        t_list = []
        d_list = []
        t_dict = dict()
        x = 0

        for day in weather['list']:
            date = day['dt']
            temp = day['main']['temp']

            d = self.convert_date(float(date))
            t = self.convert_temp(temp)

            d_list.append(d)

            if x == 0:
                t_list.append(t)

            elif str(d_list[x-1]) != d:
                last_date = d_list[x-1]
                self.sort_list(t_list)

                temps = []
                temps.append(t_list[len(t_list) - 1])  # HIGH
                temps.append(t_list[0])  # LOW

                t_dict[last_date] = temps
                t_list.clear()

            # This next bit is kind of obtuse. And ugly. And probably wasn't
            # the best way to
            # solve the problem. But it "works". So I'm keeping it. Feel free
            # to make it work
            # better.
            #
            # The problem, btw, is that the elif statement above works up
            # until the last day
            # in the forecast. Once it reaches the very end of the list, the
            # statement checks
            # if the temperature before (x-1) was on the same day as itself (x)
            # And because
            # x and x-1 are on the same date for the last temperature, it just
            # doesn't work.
            #
            # Does that make sense? No. No it does not. Sorry.
            elif x == 37:
                t_list.append(t)
                last_date = d_list[x-1]
                self.sort_list(t_list)

                temps = []
                temps.append(t_list[len(t_list) - 1])  # HIGH
                temps.append(t_list[0])  # LOW

                t_dict[last_date] = temps
                t_list.clear()

            else:
                t_list.append(t)

            x += 1

        return t_dict

    # Converts temperature from Kelvin to Fahrenheit
    def convert_temp(self, temp_kel):
        temp_fah = (temp_kel * 1.8) - 459.67
        temp_fah = math.ceil(temp_fah)
        return int(temp_fah)

    # Converts a Unix Epoch timestamp into human readable format

    def convert_date(self, date):
        new_date = time.strftime('%m/%d/%Y',  time.gmtime(date))
        # %m/%d/%Y %H:%M:%S  <--- Gives a full time string.
        return new_date

    # Bubble Sort Algorithm
    # Source: https://github.com/TheAlgorithms/Python/blob/master/sorts/
    # bubble_sort.py

    def sort_list(self, t_list):
        length = len(t_list)
        for i in range(length-1):
            swapped = False
            for j in range(length-1-i):
                if t_list[j] > t_list[j+1]:
                    swapped = True
                    t_list[j], t_list[j+1] = t_list[j+1], t_list[j]
            if not swapped:
                break

        return t_list

    # Reads the unix epoch time from time.txt file, and converts it to a
    # readable format

    def get_time(self):
        with open("time.txt", "r+") as t_file:
            time_updated = float(t_file.read())
        cd = self.convert_date(time_updated)
        return cd

    # Gets the current temperature and converts it to fahrenheit
    def get_current(self):
        current_api_call = self.call_weather("weather")
        current_res = self.make_call(current_api_call, "weather")
        current_temp_kelvin, city = self.read_weather(current_res)
        current_temp_fahrenheit = self.convert_temp(current_temp_kelvin)
        return current_temp_fahrenheit, city

    # Gets a list of dates and high/low temperatures for each day of a
    # five-day forecast.
    def get_forecast(self):
        forecast_api_call = self.call_weather("forecast")
        forecast_res = self.make_call(forecast_api_call, "forecast")
        forecast_list = self.read_forecast(forecast_res)
        return forecast_list


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def updateLabel(self, cw, t_dict, city):
        self.ui.updateLabel(cw, t_dict, city)


def main():
    weather = Weather()
    cw, city = weather.get_current()
    fw = weather.get_forecast()
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.updateLabel(cw, fw, "Rexburg")
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
