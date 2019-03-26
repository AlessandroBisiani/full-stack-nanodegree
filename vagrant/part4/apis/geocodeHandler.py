import httplib2
import json


google_client_key = ''

with open('keys.txt', 'r') as f:
    keys = f.read()
    for k in keys.split(' '):
        if k.startswith('geocode_key'):
            google_client_key = k.split('=')[-1]


def getGeocodeLocation(inputString):
    location_string = inputString.replace(" ", "+")
    google_api_key = google_client_key
    url = (
            '''https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'''
            .format(location_string, google_api_key)
            )
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    # print(url)
    # print(result)

    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']

    return latitude, longitude

if __name__ == '__main__':
    getGeocodeLocation('Tokyo, Japan')
