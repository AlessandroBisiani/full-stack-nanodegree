#original: https://github.com/udacity/APIs/blob/master/Lesson_3
#           /06_Adding%20Features%20to%20your%20Mashup/Starter%20Code/

from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

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

engine = create_engine('sqlite:///restaurants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE


@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)