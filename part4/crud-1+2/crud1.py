import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class restaurantWebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                # session = self.connect()
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<h1>Restaurants</h1>'
                output += '<a href="/restaurants/new">Add An Entry</a>'
                output += ('<br>' * 3)
                for result in restaurants:
                    output += result.name
                    output += '<br>'
                    output += '<a href="/restaurants/{}/edit">Edit</a>'.format(result.id)
                    output += '<br>'
                    output += '<a href="/restaurants/{}/delete">Delete</a>'.format(result.id)
                    output += '<br><br>'
                # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += '</body></html>'
                self.wfile.write(output)
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<h1>Make A New Restaurant</h1>'
                output += '''<form method="POST" 
                                enctype="multipart/form-data" 
                                action="/restaurants/new">'''
                output += '''
                            <input name="newRestaurantName" 
                                type="text" 
                                placeholder="New Restaurant Name"></input>
                            <input type="submit" value="Create"></input>
                            '''
                output += '</form>'
                output += '</body></html>'
                self.wfile.write(output)
                return

            if self.path.endswith('/edit'):
                id_n = self.path.split('/')[-2]
                restaurant = session.query(Restaurant).filter_by(id=id_n).one()
                # print(id_n, restaurant.name)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ''
                    output += '<html><body>'
                    output += '<h1>{}</h1>'.format(restaurant.name)
                    output += '''<form method="POST" 
                                    enctype="multipart/form-data" 
                                    action="/restaurants/{}/edit">
                            '''.format(id_n)
                    output += '''
                                <input name="modifiedRestaurantName" 
                                    type="text" 
                                    placeholder="{}"></input>
                                <input type="submit" value="Rename"></input>
                                '''.format(restaurant.name)
                    output += '</form>'
                    output += '</body></html>'
                    self.wfile.write(output)
                return
            
            if self.path.endswith('/delete'):
                id_n = self.path.split('/')[-2]
                restaurant = session.query(Restaurant).filter_by(id=id_n).one()

                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ''
                    output += '<html><body>'
                    output += '<h2>Are you sure you want to delete {}?</h2>'.format(restaurant.name)
                    output += '''<form method="POST" 
                                    enctype="multipart/form-data" 
                                    action="/restaurants/{}/delete">
                            '''.format(id_n)
                    output += '<input type="submit" value="Delete"></input>'
                    output += '</form>'
                    output += '</body></html>'
                    self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):

                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    content = fields.get('newRestaurantName')

                new_restaurant = Restaurant(name=content[0])
                session.add(new_restaurant)
                session.commit()
                
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith('/edit'):
                id_n = self.path.split('/')[-2]
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))

                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    modified_name = fields.get('modifiedRestaurantName')
                
                print(modified_name)
                
                if (modified_name[0] != '') and not modified_name[0].isspace():
                    restaurant = session.query(Restaurant).filter_by(id=id_n).one()
                    print(restaurant.id, restaurant.name)
                    restaurant.name = modified_name[0]
                    print(restaurant.id, restaurant.name)
                    session.add(restaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith('/delete'):
                id_n = self.path.split('/')[-2]
                restaurant = session.query(Restaurant).filter_by(id=id_n).one()
                
                session.delete(restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), restaurantWebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server.")
        server.socket.close()

if __name__ == '__main__':
    main()
