# You should be able to identify a Python import of another module.
# You should be able to discuss the difference in syntax between JavaScript imports and Python imports.
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animals_by_status, get_animals_by_location
from locations import get_all_locations, get_single_location, create_location, delete_location, update_location
from employees import get_all_employees, get_single_employee, create_employee, delete_employee, update_employee, get_employees_by_location
from customers import get_all_customers, get_single_customer, create_customer, delete_customer, update_customer, get_customers_by_email
import json
# CH. 1
# You should be able to identify a Python list.
# You should be able to identify a Python dictionary.
# You should be able to explain the purpose and action of a Python print() function.
# You should be able to explain that whitespace (i.e. indentation) defines scope in Python instead of {}.

# CH. 2
# You should be able to identify a Python package.
# You should be able to explain what turns a directory into a Python package.

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):

    # Here's a class function
    # self is how we reference something within this class file.
    # self = the info from HandleRequests
    def _set_headers(self, status):
        # You should be able to explain the purpose of HTTP headers.
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        # You should be able to explain the purpose of a 200 status code.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    def do_GET(self):
        # You should be able to identify a Python function.
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        # You should be able to identify a Python if block.
        # len is like .length in javascript
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = f"{get_customers_by_email(value)}"

            if key == "location_id" and resource == "employees":
                response = f"{get_employees_by_location(value)}"
            
            if key == "location_id" and resource == "animals":
                response = f"{get_animals_by_location(value)}"
            
            if key == "status" and resource == "animals":
                response = f"{get_animals_by_status(value)}"

        # encode is expecting a string, we put the responses in f strings if they are not
        # coming back as a string
        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        # You should be able to explain the purpose of a 201 status code.
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_customer = None
        new_employee = None
        new_location = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)
            # Encode the new animal and send in response
            self.wfile.write(f"{new_animal}".encode())


        if resource == "customers":
            new_customer = create_customer(post_body)
            # Encode the new customer and send in response
            self.wfile.write(f"{new_customer}".encode())


        if resource == "employees":
            new_employee = create_employee(post_body)
            # Encode the new employee and send in response
            self.wfile.write(f"{new_employee}".encode())


        if resource == "locations":
            new_location = create_location(post_body)
            # Encode the new location and send in response
            self.wfile.write(f"{new_location}".encode())



    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
            # Encode the new animal and send in response
            self.wfile.write("".encode())

        if resource == "customers":
            delete_customer(id)
            # Encode the new customer and send in response
            self.wfile.write("".encode())

        if resource == "employees":
            delete_employee(id)
            # Encode the new employee and send in response
            self.wfile.write("".encode())

        if resource == "locations":
            delete_location(id)
            # Encode the new location and send in response
            self.wfile.write("".encode())


    def do_PUT(self):
        # You should be able to explain which HTTP method is used by the client to request that a resource's state should change.
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
            # Encode the new animal and send in response
            # self.wfile.write("".encode())

        if resource == "customers":
            success = update_customer(id, post_body)
            # Encode the new customer and send in response
            # self.wfile.write("".encode())

        if resource == "employees":
            success = update_employee(id, post_body)
            # Encode the new employee and send in response
            # self.wfile.write("".encode())

        if resource == "locations":
            success = update_location(id, post_body)
            # Encode the new location and send in response

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)



        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()