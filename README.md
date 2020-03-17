# Weather
A simple python program that allows the user to enter their location, and returns the current weather at that location. 
## Use
In order to use this application, you will need an API key from openweathermap. See [this](https://openweathermap.org/api) link for more information on how to obtain an API key. 
Once you have the key, create a text file in the same directory as this program, title the file "api_key.txt", and copy your key to the file. 
Run the python file using the command line or your prefered method.
You will be asked to enter a command. To get the current weather, enter "current". To get a forecast, enter "forecast".
![Here is an example:](https://github.com/aaronpennington/Weather/blob/master/03_17_2020_screenshot.png)
## Additional Info
This project could use a lot of work. There are certain aspects that need improving. Feel free to take a look and help out any way you want! In particular, I would like to see the following: 

1. A better looking UI. The current one was designed using QT Designer, but is obviously a bit rough around the edges. 

2. Function optimization. Some parts of the code are redundant or just bad coding. I've made a note of some of these, but haven't fixed them yet. 

3. None of the weather data is stored locally, meaning that each time the program is run, an api request is made. If I run the program 5 times in one minute, 5 seperate api requests are made. Since the weather really doesn't change that frequently, keeping data in a file could be wise. 

Thanks!
