# original: https://github.com/udacity/APIs/blob/master/Lesson_3
#           /06_Adding%20Features%20to%20your%20Mashup/Starter%20Code/

from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request, flash, redirect, url_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
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


@app.route('/restaurants', methods=['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[r.serialize for r in restaurants])

    elif request.method == 'POST':
        location = request.args.get('location')
        mealType = request.args.get('mealType')
        r_dict = findARestaurant(mealType, location)

        pre_existent_entry = session.query(Restaurant).filter_by(
                restaurant_name=r_dict['name'],
                restaurant_address=r_dict['address']).first()

        # Check the restaurant hasn't already been added.
        # Return it without adding to the db, if it has.
        if pre_existent_entry is None:
            new_Restaurant = Restaurant(
                    restaurant_name=r_dict['name'],
                    restaurant_address=r_dict['address'],
                    restaurant_image=r_dict['image']
                    )
            print('\r\n---------------created the restaurant')
            # print(r_dict['name'], r_dict['address'], r_dict['image'])
            session.add(new_Restaurant)
            session.commit()
            # print('New restaurant added to the database.')
            return jsonify(new_Restaurant.serialize)
        else:
            return jsonify(pre_existent_entry.serialize)
    else:
        return '{} not supported at this endpoint'.format(request.method)


@app.route('/restaurants/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_handler(id):
    if request.method == 'GET':
        try:
            restaurant = session.query(Restaurant).filter_by(id=id).one()

        except NoResultFound:
            return redirect(url_for('all_restaurants_handler'))
        except Exception as ex:
            flash(str(ex))
            return redirect(url_for('all_restaurants_handler'))
        else:
            return jsonify(restaurant.serialize)

    elif request.method == 'PUT':

        r_name = request.args.get('name')
        r_address = request.args.get('address')
        r_image = request.args.get('image')
        # print(r_name, r_location, r_image)
        if r_name and r_address and r_image:
            try:
                restaurant = session.query(Restaurant).filter_by(id=id).one()
                restaurant.restaurant_name = r_name
                restaurant.restaurant_address = r_address
                restaurant.restaurant_image = r_image
                session.add(restaurant)
                session.commit()

            except NoResultFound:
                # print('1 ~~~~~~~~~~~~~~~~~~~~')
                return redirect(url_for('all_restaurants_handler'))
            except Exception as ex:
                flash(str(ex))
                # print('2 ~~~~~~~~~~~~~~~~~~~~')
                return redirect(url_for('all_restaurants_handler'))
            else:
                return jsonify(restaurant.serialize)
        else:
            # print('3 ~~~~~~~~~~~~~~~~~~~~')
            return redirect(url_for('all_restaurants_handler'))

    elif request.method == 'DELETE':
        try:
            restaurant = session.query(Restaurant).filter_by(id=id).one()
            session.delete(restaurant)
            session.commit()

        except NoResultFound:
            return redirect(url_for('all_restaurants_handler'))
        except Exception as ex:
            flash(str(ex))
            return redirect(url_for('all_restaurants_handler'))
        else:
            return 'Restaurant {} deleted'.format(id)

    else:
        return '{} not supported at this endpoint'.format(request.method)


if __name__ == '__main__':
    app.secret_key = 'Troubling troubadours'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
