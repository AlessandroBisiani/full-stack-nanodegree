from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#API Endpoint (GET)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(menu_item.serialize)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
    return render_template('menu.html', restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('newmenuitem.html', restaurant=restaurant)
    if request.method =='POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    return "Request Not Supported"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method =='GET':
        menu_item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, item = menu_item)
    if request.method =='POST':
        item_to_edit = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
        item_to_edit.name = request.form['name']
        session.add(item_to_edit)
        session.commit()
        flash("Menu Item Edited")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    return "Request Not Supported"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletionItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'GET':
        return render_template('deletemenuitem.html', item = deletionItem)
    if request.method == 'POST':
        session.delete(deletionItem)
        session.commit()
        flash("Menu Item Deleted")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    return "Request Not Supported"

if __name__ == '__main__':
    app.secret_key = 'secret'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
