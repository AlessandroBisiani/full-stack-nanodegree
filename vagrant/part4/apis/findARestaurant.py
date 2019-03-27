from geocodeHandler import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = ''
foursquare_client_secret = ''
google_client_key = ''


with open('keys.txt', 'r') as f:
    keys = f.read()
    for k in keys.split(' '):
        if k.startswith('client_id'):
            foursquare_client_id = k.split('=')[-1]
        elif k.startswith('client_secret'):
            foursquare_client_secret = k.split('=')[-1]
        elif k.startswith('geocode_key'):
            google_client_key = k.split('=')[-1]

# print(google_client_key, foursquare_client_id)

def findARestaurant(meal_type, location):
    # print(foursquare_client_id, foursquare_client_secret, google_client_key)
    # Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    lat, lon = getGeocodeLocation(location)
    # print(lat, lon)
    # Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    url = (
            'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&v=20130815&ll={},{}&query={}'.format(foursquare_client_id, foursquare_client_secret, lat, lon, meal_type)
            )
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)

    if result['response']['venues'][0]:
        # Grab the first restaurant
        restaurant = result['response']['venues'][0]
        id = restaurant['id']
        name = restaurant['name']
        address = restaurant['location']['formattedAddress']
        full_address = ''
        for line in address:
            full_address += line + ' '
        # Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        photo_url = 'https://api.foursquare.com/v2/venues/{}/photos?limit=1&v=20130815&client_id={}&client_secret={}'.format(id, foursquare_client_id, foursquare_client_secret)
        response, content = h.request(photo_url, 'GET')
        result = json.loads(content)

        # Grab the first image
        image_url = ''
        if result['response']['photos']['items']:
            img = result['response']['photos']['items'][0]
            image_url = '{}cap300x300{}'.format(img['prefix'], img['suffix'])
            # print(image_url)
        else:
        # If no image is available, insert default a image url
            image_url = 'https://media-cdn.grubhub.com/image/upload/c_scale,w_1350/q_50,dpr_auto,f_auto,fl_lossy,c_crop,e_vibrance:20,g_center,h_900,w_800/e_gradient_fade,y_0.15,b_rgb:5C6062/v1553024666/prod/promo/Tbell-NewHP-1.jpg'

        # Return a dictionary containing the restaurant name, address, and image url
        restaurant_dict = {'name':name, 'address':full_address, 'image':image_url}
        # print('\r\nRestaurant Name: %s' % name)
        # print('Address: %s' % full_address)
        # print('Relevant Image: %s\r\n' % image_url)
        # print(repr('\r\n{}\r\n{}\r\n{}\r\n')).format(restaurant_dict['name'], restaurant_dict['address'], restaurant_dict['image'])
        return restaurant_dict
    else:
        return 'No Restaurants Found'

if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney, Australia")
