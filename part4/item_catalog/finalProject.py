from flask import Flask, render_template
app = Flask(__name__)


# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {
    'name': 'Blue Burgers', 'id': '2'}, {'name': 'Taco Hut', 'id': '3'}]


# Fake Menu Items
items = [{'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'}, {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert', 'id': '2'}, {'name': 'Caesar Salad', 'description':
                                                                                                                                                                                                                                                        'with fresh organic vegetables', 'price': '$5.99', 'course': 'Entree', 'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'}, {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer', 'id': '5'}]
item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese',
'price': '$5.99', 'course': 'Entree'}


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return render_template('restaurants.html')

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
def showMenu():
    return render_template('menu.html')

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem():
    return render_template('newMenuItem.html')

@app.route('/restaurant/<int:restaurant_id>/menu/edit')
def editMenuItem():
    return render_template('editMenuItem.html')

@app.route('/restaurant/<int:restaurant_id>/menu/delete')
def deleteMenuItem():
    return render_template('deleteMenuItem.html')



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)