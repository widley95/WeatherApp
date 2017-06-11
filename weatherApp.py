
# Author: Ley Nezifort
# Created on : Jun 9, 2017

import urllib.request
import urllib.parse
import sys
import json
import math

def main ():
    #API_key from Open Weahter Map
    api_key = "e9b3a3d3af381d3ae344456e8c542777"
    #base URL to be used for the request 
    url_base = "http://api.openweathermap.org/data/2.5/weather?"
    
    if (len(sys.argv) <2): 
        # Get a location from user if it wasn't given
        # from the command line
        location = input("Please enter a location: ")
    else:
        # Save the location entered from the command line
        location = sys.argv[1]

    params = {"appid" : api_key, "units" : "imperial", }
    # Check if the location is a zip code 
    if location.isdigit():
        # make sure the location entered is of 5 digits 
        if (len(location) == 5):
            params["zip"] = location
            # Encode URL request with the parameters
            url = url_base + urllib.parse.urlencode(params)
            getData(url)

        else:
            print("The Zip code must have 5 Digits") 
            quit()
    # if the location is a city 
    else:
        params["q"] = location
        url = url_base + urllib.parse.urlencode(params)
        getData(url)
    
    
def getData(url):
    response = urllib.request.urlopen(url)
    raw_data = response.read()
    json_data = json.loads(raw_data.decode('utf-8'))
    city_name = json_data["name"]
    weather_data = json_data["main"]
    current_temp = round(weather_data["temp"], 1)
    print("It is currently {} degrees in {}".format(current_temp, city_name))




if __name__ == "__main__" : main()