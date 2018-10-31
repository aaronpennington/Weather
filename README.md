# Weather
A simple python program that allows the user to enter their location, and returns the current weather at that location. 
## Use
In order to use this application, you will need an API key from openweathermap. See [this](https://openweathermap.org/api) link for more information on how to obtain an API key. 
Once you have the key, create a text file in the same directory as this program, title the file "api_key.txt", and copy your key to the file. 
Run the python file using the command line or your prefered method.
You will be asked to enter a command. To get the current weather, enter "current". To get a forecast, enter "forecast".
![Here is an example:](https://github.com/aaronpennington/Weather/blob/master/output.PNG)
## Additional Info
Currently, the program has several limitations, including (but not limited to): 

1. The forecast feature is very limited.

2. There is no GUI. 

3. The weather information is not stored in any way, meaning that the client must call the website every time a weather request is made. This is fine if the client makes a request once every few minutes, but is overkill if the client makes several requests in a very short period of time. 

Thanks!
