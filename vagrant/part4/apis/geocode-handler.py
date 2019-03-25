import httplib2
import json


def todoAPIKey:
    return '''geocode_handler.py TODO: Add google geocode API user
            key in production'''


def getGeocodeLocation(inputString):
    location_string = inputString.replace(" ", "+")
    google_api_key = todoAPIKey()
    url = (
            '''https://maps.googleapis.com/maps/api/geocode/json
            ?address={}&key={}'''.format(location_string, google_api_key)
            )
