from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    try:
        restaurants = session.query(Restaurant).all()
    except Exception as e:
        return str(e)
    else:
        return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/')
def newRestaurant():
    return render_template('newRestaurant.html')

@app.route('/restaurant/restaurant_id/edit')
def editRestaurant():
    return render_template('editRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant():
    return render_template('deleteRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    if request.method == 'GET':
        try:
            restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
            items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
            return render_template('menu.html', restaurant = restaurant, items = items)
        except Exception as e:
            return str(e)
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
            flash("New Menu Item Created")
        except Exception as e:
            return str(e)
        else:
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/edit')
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
        except Exception as e:
            return str(e)
        else:
            flash("Menu Item Edited")
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

@app.route('/restaurant/<int:restaurant_id>/menu/<menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    try:
        deletionItem = session.query(MenuItem).filter_by(id = menu_id).one()
    except Exception as e:
        return str(e)
    if request.method == 'GET':
        return render_template('deletemenuitem.html', item = deletionItem)
    elif request.method == 'POST':
        try:
            session.delete(deletionItem)
            session.commit()
            flash("Menu Item Deleted")
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
        except Exception as e:
            return str(e)
    else:
        flash('Method "{}" Not Supported'.format(request.method))
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

if __name__ == '__main__':
    app.secret_key = 'secret'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)