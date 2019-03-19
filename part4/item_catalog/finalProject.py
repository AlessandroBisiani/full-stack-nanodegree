from flask import flask
app = Flask(__name__)


@app.route('/')
@app.route('/retaurants')
def showRestaurants():
    return "This page will return all my restaurants"

@app.route('/restaurant/new/')
def newRestaurant():
    return "This page will be for making a new Restaurant"

@app.route('/restaurant/restaurant_id/edit')
def editRestaurant():
    return "Edit restaurant Page"

@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant():
    return "Delete restaurant page"

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu():
    return "Show Menu Page"

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem():
    return " New Menu Item Page"

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def editMenuItem():
    return "Edit menu item page"

@app.route('/restaurant/<int:restaurant_id>/menu/new')
def deleteMenuItem():
    return "delete menu item page"



if __name__ == '__main__':
    app.debug = True
    app.run(host = 0.0.0.0, port = 5000)