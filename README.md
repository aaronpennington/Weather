# Weather
A simple python program that allows the user to enter their location, and returns the current weather at that location. 
## Use
In order to use this application, you will need an API key from openweathermap. See [this](https://openweathermap.org/api) link for more information on how to obtain an API key. 
Once you have the key, create a text file in the same directory as this program, title the file "api_key.txt", and copy your key to the file. 
## Additional Info
Currently, the program has several limitations, including (but not limited to): 

1. only displaying current weather, not a forecast; 

~~2. unable to differentiate between multiple cities with the same name (so Birmingham, USA is the same as Birmingham, UK in the program), leading to wildly inaccurate weather reports;~~

~~3. only able to get weather for cities or locations included in the city.json file, which is provided by openweathermap and contains a really large list of cities;~~

(#2-3 have been resolved. Location is now based on latitude & longitude, not a user inputed city name.)

I plan to overcome these limitations soon, but would appreciate any feedback. There may be other bugs that I am unaware of. 

Thanks!
