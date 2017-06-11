
# Author: Ley Nezifort
# Created on : Jun 9, 2017

import urllib.request
import urllib.parse
import sys
import json

def main ():
    #API_key from Open Weahter Map
    weather_api_key = "e9b3a3d3af381d3ae344456e8c542777"
    # Api_Key from google 
    google_api_key = "AIzaSyCaGVA3zxRjmfjqqoU1aWN5RpmHky-G03Y"
    #base URL to be used for the request to get the weather info
    weather_url_base = "http://api.openweathermap.org/data/2.5/weather?"
    #base URL to be used for the request to get the state 
    google_url_base ="https://maps.googleapis.com/maps/api/geocode/json?"
    
    
    if (len(sys.argv) <2): 
        # Get a location from user if it wasn't given
        # from the command line
        location = input("Please enter a location: ")
    else:
        # If a location was given from the command line, save it
        location = sys.argv[1]

    weather_request_params = {"appid" : weather_api_key, "units" : "imperial" }
    # Check if the location is a zip code 
    if location.isdigit():
        # make sure the location entered is of 5 digits 
        if (len(location) == 5):
            weather_request_params["zip"] = location
            # Encode URL request with the parameters
            weather_url = weather_url_base + urllib.parse.urlencode(weather_request_params)
            # Get the weather information
            results = getData(weather_url)
            # Encode HTTP request 
            # Will be used to look up state from longitude & latitude coordinates
            google_url = google_url_base + "&latlng=" +str(results["lat"]) + "," + str(results["lng"]) + "&key=" + google_api_key
            # Look up the state 
            results["state"] = getState(google_url)
            # Print info to the user 
            print("It is currently {} degrees in {}, {}".format(results["current_temp"], results["city"], results["state"]))

        # Invalid Zip Code 
        else:
            print("The Zip code must have 5 Digits") 
            quit()
    # if the location is a city / State
    else:
        weather_request_params["q"] = location
        # Encode HTTP request 
        weather_url = weather_url_base + urllib.parse.urlencode(weather_request_params)
        # Get the weather information 
        results = getData(weather_url)
        # Encode HTTP request; will be used to look up state from google maps api
        google_url = google_url_base + "&latlng=" +str(results["lat"]) + "," + str(results["lng"]) + "&key=" + google_api_key
        # Look up the state 
        results["state"] =getState(google_url)
        # Print info to the user 
        print("It is currently {} degrees in {}, {}".format(results["current_temp"], results["city"], results["state"]))

# Send a HTTP request to the Open Weather app server
# and parse through the Json formatted response 
def getData(url):
    try: 
        # send the request 
        response = urllib.request.urlopen(url)
        raw_data = response.read()
        # Convert the format of the response to JSon 
        json_data = json.loads(raw_data.decode('utf-8'))
        # get the name of the city 
        city = json_data["name"]
        # get the longitude & latitude to be used in later request
        longitude = json_data["coord"]["lon"]
        latitude = json_data["coord"]["lat"]
        # get the weather information 
        weather_data = json_data["main"]
        current_temp = int (round(weather_data["temp"], 1))
        # Save all the results in a dictionary 
        results = {"current_temp" : current_temp, "city" : city, "lat" : latitude, "lng" : longitude}
        return results
    except:
        print("An error occured while getting the weather info. Please verify the location entered")
        quit()
     
# Send a HTTP request to google maps api 
# to look up state given lat & lng 
def getState(url):
    try: 
        # Send the request 
        response = urllib.request.urlopen(url)
        raw_data = response.read()
        # Convert the response to JSon
        json_data = json.loads(raw_data.decode('utf-8'))
        # Extract needed data from response 
        location_info= json_data["results"][0]["address_components"]
        # Following line is just to get the state :/ 
        counter = -1
        state = ""
        for d in location_info:
            counter = counter + 1
            if d["types"][0] == "administrative_area_level_1":
                state = d["short_name"]
                break
        return state
    
    except:
        print("Ooops something went wrong! ")
        quit()
    


if __name__ == "__main__" : main()