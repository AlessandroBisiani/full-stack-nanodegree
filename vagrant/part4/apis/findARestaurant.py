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
# 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    lat, lon = getGeocodeLocation(location)
    # print(lat, lon)
# 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
# HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = (
            'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&v=20130815&ll={},{}&query={}'.format(foursquare_client_id, foursquare_client_secret, lat, lon, meal_type)
            )
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)

    if result['response']['venues'][0]:
        # 3. Grab the first restaurant
        restaurant = result['response']['venues'][0]
        id = restaurant['id']
        name = restaurant['name']
        address = restaurant['location']['formattedAddress']
        full_address = ''
        for line in address:
            full_address += line
        # 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
        photo_url = 'https://api.foursquare.com/v2/venues/{}/photos?limit=1&v=20130815&client_id={}&client_secret={}'.format(id, foursquare_client_id, foursquare_client_secret)
        response, content = h.request(photo_url, 'GET')
        result = json.loads(content)

        # 5. Grab the first image
        image_url = ''
        if result['response']['photos']['items']:
            img = result['response']['photos']['items'][0]
            image_url = '{}cap300x300{}'.format(img['prefix'], img['suffix'])
            # print(image_url)
        else:
        # 6. If no image is available, insert default a image url
            image_url = 'https://media-cdn.grubhub.com/image/upload/c_scale,w_1350/q_50,dpr_auto,f_auto,fl_lossy,c_crop,e_vibrance:20,g_center,h_900,w_800/e_gradient_fade,y_0.15,b_rgb:5C6062/v1553024666/prod/promo/Tbell-NewHP-1.jpg'

        # 7. Return a dictionary containing the restaurant name, address, and image url
        restaurant_dict = {'name':name, 'address':address, 'image':image_url}
        print('\r\nRestaurant Name: %s' %name)
        print('Address: %s' %full_address)
        print('Relevant Image: %s\r\n' %image_url)
        # print(repr('\r\n{}\r\n{}\r\n{}\r\n')).format(rest_dict['name'], rest_dict['address'], rest_dict['image'])
        return restaurant_dict
    else:
        print 'No Restaurants Found'
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






# from geocodeHandler import getGeocodeLocation
# import json
# import httplib2

# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# foursquare_client_id = "X1BNTCLGXDLM3RHOKR25S5ZZZBQ1JQOJ1CLMH2IK4FR5GZOB"
# foursquare_client_secret = "W4YQ2TOKNUBBUVUYQRS1ZZS0L5Q3D5B5N5OLMMVCREURRSVL"


# def findARestaurant(mealType,location):
# 	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
# 	latitude, longitude = getGeocodeLocation(location)
# 	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
# 	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
# 	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s' % (foursquare_client_id, foursquare_client_secret,latitude,longitude,mealType))
# 	h = httplib2.Http()
# 	result = json.loads(h.request(url,'GET')[1])
	
# 	if result['response']['venues']:
# 		#3.  Grab the first restaurant
# 		restaurant = result['response']['venues'][0]
# 		venue_id = restaurant['id'] 
# 		restaurant_name = restaurant['name']
# 		restaurant_address = restaurant['location']['formattedAddress']
# 		address = ""
# 		for i in restaurant_address:
# 			address += i + " "
# 		restaurant_address = address
# 		#4.  Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
# 		url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20150603&client_secret=%s' % ((venue_id,foursquare_client_id,foursquare_client_secret)))
# 		result = json.loads(h.request(url, 'GET')[1])
# 		#5.  Grab the first image
# 		if result['response']['photos']['items']:
# 			firstpic = result['response']['photos']['items'][0]
# 			prefix = firstpic['prefix']
# 			suffix = firstpic['suffix']
# 			imageURL = prefix + "300x300" + suffix
# 		else:
# 			#6.  if no image available, insert default image url
# 			imageURL = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
# 		#7.  return a dictionary containing the restaurant name, address, and image url
# 		restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':imageURL}
# 		print "Restaurant Name: %s" % restaurantInfo['name']
# 		print "Restaurant Address: %s" % restaurantInfo['address']
# 		print "Image: %s \n" % restaurantInfo['image']
# 		return restaurantInfo
# 	else:
# 		print "No Restaurants Found for %s" % location
# 		return "No Restaurants Found"

# if __name__ == '__main__':
# 	findARestaurant("Pizza", "Tokyo, Japan")
# 	findARestaurant("Tacos", "Jakarta, Indonesia")
# 	findARestaurant("Tapas", "Maputo, Mozambique")
# 	findARestaurant("Falafel", "Cairo, Egypt")
# 	findARestaurant("Spaghetti", "New Delhi, India")
# 	findARestaurant("Cappuccino", "Geneva, Switzerland")
# 	findARestaurant("Sushi", "Los Angeles, California")
# 	findARestaurant("Steak", "La Paz, Bolivia")
# findARestaurant("Gyros", "Sydney, Australia")