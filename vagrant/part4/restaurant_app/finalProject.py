#! /usr/bin/env python3
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/JSON')
def showRestaurantsJSON():
    try:
        restaurants = session.query(Restaurant).all()
    except Exception as e:
        return str(e)
    else:
        return jsonify(Restaurants = [r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
    menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(Menu = [item.serialize for item in menu])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
    return jsonify(item.serialize)

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    if request.method == 'GET':
        try:
            restaurants = session.query(Restaurant).all()
        except Exception as e:
            return str(e)
        else:
            return render_template('restaurants.html',
                                   restaurants = restaurants)
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/new/', methods = ['GET', 'POST'])
def newRestaurant():
    if request.method == 'GET':
        return render_template('newRestaurant.html')
    elif request.method == 'POST':
        try:
            newRestaurant = Restaurant(name = request.form['name'])
            session.add(newRestaurant)
            session.commit()
        except Exception as e:
            return str(e)
        else:
            return redirect(url_for('showRestaurants'))
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'GET':
        try:
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        except Exception as e:
            return str(e)
        else:
            return render_template('editRestaurant.html', restaurant = restaurant)
    elif request.method == 'POST':
        try:
            restaurant_edit = session.query(Restaurant).filter_by(id = restaurant_id).one()
            oldName = restaurant_edit.name[:]
            newName = request.form['newName']
            restaurant_edit.name = newName
            session.add(restaurant_edit)
            session.commit()
            flash('{} changed to {}'.format(oldName, newName))
        except Exception as e:
            return str(e)
        else:
            return redirect(url_for('showRestaurants'))
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    try:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    except Exception as e:
        return str(e)
    else:
        if request.method == 'GET':
            return render_template('deleteRestaurant.html', restaurant = restaurant)
        elif request.method == 'POST':
            try:
                name = restaurant.name[:]
                session.delete(restaurant)
                session.commit()
                menu_delete = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
                for mItem in menu_delete:
                    iName = mItem.name[:]
                    session.delete(mItem)
                    session.commit()
                    flash("{} deleted".format(iName))
                flash('You deleted {}'.format(name))
            except Exception as e:
                return str(e)
            else:
                return redirect(url_for('showRestaurants'))
        else:
            flash('Method "{}" Not Supported'.format(request.method))
            return redirect(url_for('showRestaurants'))

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    if request.method == 'GET':
        try:
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
            items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
        except Exception as e:
            return str(e)
        else:
            return render_template('menu.html', restaurant = restaurant, items = items)
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        try:
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        except Exception as e:
            return str(e)
        else:
            return render_template('newMenuItem.html', restaurant=restaurant)
    elif request.method =='POST':
        try:
            newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
            session.add(newItem)
            session.commit()
            flash('New Menu Item Created')
        except Exception as e:
            return str(e)
        else:
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method =='GET':
        try:
            menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
        except Exception as e:
            return str(e)
        else:
            return render_template('editmenuitem.html', restaurant_id = restaurant_id, item = menu_item)
    elif request.method =='POST':
        try:
            item_to_edit = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
            item_to_edit.name = request.form['name']
            session.add(item_to_edit)
            session.commit()
            flash('Edited menu item')
        except Exception as e:
            return str(e)
        else:
            flash("Menu Item Edited")
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    try:
        deletionItem = session.query(MenuItem).filter_by(id = menu_id).one()
    except Exception as e:
        return str(e)
    else:
        if request.method == 'GET':
            return render_template('deletemenuitem.html', item = deletionItem)
        elif request.method == 'POST':
            try:
                session.delete(deletionItem)
                session.commit()
                flash("Menu Item Deleted")
            except Exception as e:
                return str(e)
            else:
                return redirect(url_for('showMenu', restaurant_id = restaurant_id))
        else:
            flash('Method "{}" Not Supported'.format(request.method))
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))

if __name__ == '__main__':
    app.secret_key = 'secret'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
