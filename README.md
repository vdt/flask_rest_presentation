# Creating A Simple REST API with Python

This is a presentation about creating a simple REST API using Python, the Flask micro web framework and Swagger to provide documenation about the API. Our REST API will be serving a *simple* names data structure where the names are keyed to the last name, and any updates are marked as timestamp changes. This data could be backed to a database, saved in a file, accessible through some network protocol, but in our case is just an in-memory data structure. The purpose of the API is to decouple how the data exists from how it is used, and therefore hides the data implementation details.

The API will present a simple **CRUD** interface that maps to HTTP methods like this:

* Create -  POST
* Read -    GET
* Update -  PUT
* Delete -  DELETE

## Let's Get Started

First we'll create a simple web server using the Flask Micro Framework. The Python code below gets a very basic web server up and running that will respond with *Hello World* when a request for the home page comes in.

```python
# import Flask, the Python micro web framework
from flask import Flask

# create the application instance
app = Flask(__name__)

# create a URL route in our application for "/"
@app.route('/')
def hello_world():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the string "Hello World!"
    """
    return 'Hello World!'


# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)

```

Nothing very exciting going on here. We import the Flask module, giving our application access to the Flask functionality. We then create a Flask application instance, the *app* variable. Next we connect a URL route to the *hello_world()* function. This connects an HTTP GET / request to the *hello_world()* function, the return value is sent back to the browser making the request. And lastly, we run the application, which starts the server that waits for requests and dispatches them to know routes.

## Let's Add Template Processing

Let's make our web application a little more flexible by allowing it to process and deliver templtes. This let's us serve an *index.html* file rather than having to include all the HTML in the Python application itself. Flask has this ability built in, so we'll modify our program to use this functionality.

```python

# import Flask, the Python micro web framework
from flask import (
    Flask,
    render_template
)

# create the application instance
app = Flask(__name__,
            template_folder="templates")


# create a URL route in our application for "/"
@app.route('/')
def hello_world():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template "index.html"
    """
    return render_template("index.html")


# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
```

We've modified our code to include the additional Flask function *render_template*. We then modified our application creation by telling Flask where we're storing our template files. In this case just in a new folder called *templates*, not very original, but certainly very clear.

Now in our *hello_world()* function we change the code so that rather than returning just the string "Hello World", it returns the results of calling *render_template("index.html")*. As you might guess, the *render_template()* function gets the file index.html from the templates folder, renders it, and returns it to the requesting browser. The index.html file is just a plain HTML file build to display "Hello World" on the browser.

I added template processing to use later to display an example web application that uses the REST API that we're about to build.

## Adding a GET Request Handler

Now let's add a REST GET request handler to our appliation. First we'll need some data to actually have our API serve, in this case will be a simple in-memory data structure. We'll also make use of another Python module, called flask_restful, which makes it easy to create REST APIs systems in Python. Here's our modified code:

```python
# import python module to create timestamp
from datetime import datetime

# import Flask, the Python micro web framework
from flask import (
    Flask,
    render_template
)

# import the Flask API package
from flask_restful import Resource, Api

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# data to serve with our API
LIST_OF_NAMES = {
    "Farrell": {"fname": "Doug", "lname": "Farrell", "timestamp": get_timestamp()},
    "Murphy": {"fname": "Kevin", "lname": "Murphy", "timestamp": get_timestamp()},
    "Easter": {"fname": "Bunny", "lname": "Easter", "timestamp": get_timestamp()},
    "Burglar": {"fname": "Ham", "lname": "Burglar", "timestamp": get_timestamp()},
    "Nye": {"fname": "Bill", "lname": "Nye", "timestamp": get_timestamp()}
}

class NamesList(Resource):
    """
    Our NameList API
    """
    def __init__(self):
        """
        Let's create some data for our API to serve
        """
        self.names = LIST_OF_NAMES

    def get(self):
        """
        This method responds to an HTTP GET request and
        retrieves the entire list.
        """
        return [record for record in self.names.values()]


# create the application instance
app = Flask(__name__,
            template_folder="templates")

# connect the flask restful system into the application
api = Api(app)

# connect our API class into the API processing connection
api.add_resource(NamesList, "/api/names")

# create a URL route in our application for "/"
@app.route('/')
def hello_world():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template "index.html"
    """
    return render_template("index.html")

# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
```
 
Here we've added the flask_restful module, importing the particular functionality *Resource* and *Api*. We've also created the helper function *get_timestamp()* that just generates a string respresenation of a current timestamp. This is used to create our in-memory structure, and to modify the data when we start modifying it with the API. 

We then create our **LIST_OF_NAMES** data structure, which is just a simple names database, keyed on the last name. This is a global variable so it's state persists between REST API calls.

Then we actually add some REST API functionality. The class *NamesList(Resource)* defines our REST API handler by inheriting from the Resource object we imported earlier. Our class only implements a GET handler to start with, which returns the entire **LIST_OF_NAMES** data structure. 

We also chain our the flask_restful *Api* functionality we imported earlier into the application instance *app*. This connects our API processing into the request handler so it can respond to routes, which we'll define next.

Lastly we map our class *NamesList* to a route. This connects a class instance to the request processing, and will get called for GET /api/names

Running this code the browser will display the **LIST_OF_NAMES** on the screen if we navigate to localhost:5000/api/names, and will look like this:

```javascript
[
    {
        "fname": "Ham", 
        "lname": "Burglar", 
        "timestamp": "2016-07-27 11:42:38"
    }, 
    {
        "fname": "Doug", 
        "lname": "Farrell", 
        "timestamp": "2016-07-27 11:42:38"
    }, 
    {
        "fname": "Bunny", 
        "lname": "Easter", 
        "timestamp": "2016-07-27 11:42:38"
    }, 
    {
        "fname": "Kevin", 
        "lname": "Murphy", 
        "timestamp": "2016-07-27 11:42:38"
    }, 
    {
        "fname": "Bill", 
        "lname": "Nye", 
        "timestamp": "2016-07-27 11:42:38"
    }
]
```

# Building Out Our Complete REST API

Building on our program we extend it to provide a complete REST API for the URL /api/names. This involves two steps. The class *NamesList* gets the additional REST method *post()*, and this completes this class. Notice that both get and post in this class respond to /api/names (no additional URL information). 

To provide the complete REST API we need to also respond to /api/names/<last_name>, which will handle working with one name record in our data structure. We do this by creating another class *Names(Resource)*, which we map to /api/names/<string:last_name> with this line of code:

```python
api.add_resource(Names, "/api/names/<string:last_name>")
```

Here is our modified code:

```python
# import python module to create timestamp
from datetime import datetime

# import Flask, the Python micro web framework
from flask import (
    Flask,
    render_template,
    request
)

# import the Flask API package
from flask_restful import (
    Resource,
    Api,
    abort
)

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# data to serve with our API
LIST_OF_NAMES = {
    "Farrell": {"fname": "Doug", "lname": "Farrell", "timestamp": get_timestamp()},
    "Murphy": {"fname": "Kevin", "lname": "Murphy", "timestamp": get_timestamp()},
    "Easter": {"fname": "Bunny", "lname": "Easter", "timestamp": get_timestamp()},
    "Burglar": {"fname": "Ham", "lname": "Burglar", "timestamp": get_timestamp()},
    "Nye": {"fname": "Bill", "lname": "Nye", "timestamp": get_timestamp()}
}

class Names(Resource):
    """
    Our Name API
    """
    def __init__(self):
        """
        Let's connect to some data for our API to serve
        """
        self.names = LIST_OF_NAMES

    def get(self, last_name):
        """Get a name record"""
        # did we get an endpoint parameter?
        if last_name is not None:
            if last_name in self.names:
                retval = self.names.get(last_name)

        # otherwise, nope, didn't find the resource
        else:
            abort(404, )

        return retval

    def put(self, last_name):
        """Update a name record"""
        record = None

        # did we get a valid name?
        if last_name in self.names:
            # get the PUT JSON data
            put_data = request.get_json()

            record = self.names.get(last_name)
            record["lname"] = put_data.get("lname", record["lname"])
            record["fname"] = put_data.get("fname", record["fname"])
            record["timestamp"] = get_timestamp()

        # otherwise, nope, didn't find the record
        else:
            abort(404)

        # return the updated record
        return record, 201

    def delete(self, last_name):
        """
        This method responds to an HTTP DELETE entry,
        and removes an entry from the names list based on the
        passed last name
        """
        # did we get a valid name?
        if last_name in self.names:
            del self.names[last_name]

        # otherwise, nope, didn't find the record
        else:
            abort(404)

        return "", 204

class NamesList(Resource):
    """
    Our NameList API
    """
    def __init__(self):
        """
        Let's create some data for our API to serve
        """
        self.names = LIST_OF_NAMES

    def get(self):
        """
        This method responds to an HTTP GET request and
        retrieves the entire list.
        """
        return [record for record in self.names.values()]

    def post(self):
        """
        This method responds to an HTTP POST request,
        with a message body that creates a new entry
        in the names list
        """
        # get the POST JSON data
        post_data = request.get_json()

        # update the post_data with current timestamp
        post_data["timestamp"] = get_timestamp()

        # update the list of names
        self.names[post_data["lname"]] = post_data

        # return the newly created record
        return post_data, 201

# create the application instance
app = Flask(__name__,
            template_folder="templates")

# connect the flask restful system into the application
api = Api(app)

# connect our API class into the API processing connection
api.add_resource(NamesList, "/api/names")
api.add_resource(Names, "/api/names/<string:last_name>")

# create a URL route in our application for "/"
@app.route('/')
def hello_world():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template "index.html"
    """
    return render_template("index.html")

# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
```

I've added web application code to this version of the application in the form of a more fully formed home page and some custom JavaScript. Let's take a look at this application.

## Adding Swagger Documentation To The API

[Swagger](http://swagger.io/) is a specification for documenating a REST API with information and providing working examples. This is useful when using an API as a developer can "try the API out" without having to build a test harness application. This helps get a leg up on how the API works, what it expects and how the developer can make use of it.

We can extend our application to provide Swagger documenation by making use of another module, called flask_restful_swagger. This gives functionality to inject our documenation into our REST API methods, and have the system process and use this documenation to meet the Swagger spec and display the documenation.

To use the Swagger system we decorate our REST API methods with a call to *@swagger.operation(...)* A decorator in Python is a way of 'wrapping' a function with additional functionality without having to modify the decorated function, and is indicated by the *'@'* symbol. Here's our application decorated with Swagger documenation:

```python
# import python module to create timestamp
from datetime import datetime

# import Flask, the Python micro web framework
from flask import (
    Flask,
    render_template,
    request
 )

# import the Flask API package
from flask_restful import (
    Resource,
    Api,
    abort
)
from flask_restful_swagger import swagger


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# data to serve with our API
LIST_OF_NAMES = {
    "Farrell": {"fname": "Doug", "lname": "Farrell", "timestamp" :get_timestamp()},
    "Murphy": {"fname": "Kevin", "lname": "Murphy", "timestamp": get_timestamp()},
    "Easter": {"fname": "Bunny", "lname": "Easter", "timestamp": get_timestamp()},
    "Burglar": {"fname": "Ham", "lname": "Burglar", "timestamp": get_timestamp()},
    "Nye": {"fname": "Bill", "lname": "Nye", "timestamp": get_timestamp()}
}


class Names(Resource):
    """
    Our Name API
    """
    def __init__(self):
        """
        Let's connect to some data for our API to serve
        """
        self.names = LIST_OF_NAMES

    @swagger.operation(
        notes='This method gets the requested name from the data structure',
        nickname='Read',
        parameters=[
            {
                'name': 'last_name',
                'description': 'The last name of the name record to retrieve',
                'required': True,
                'dataType': 'string',
                'paramType': 'path'
            }
        ],
        responseMessages=[
            {
                'code': 200,
                'message': 'Retrieved the requested name'
            }
        ]
    )
    def get(self, last_name):
        """Get a name record"""
        # did we get an endpoint parameter?
        if last_name is not None:
            if last_name in self.names:
                retval = self.names.get(last_name)

        # otherwise, nope, didn't find the resource
        else:
            abort(404, )

        return retval

    @swagger.operation(
        notes='update a name in the data structure',
        nickname='Update',
        contentType='application/json',
        parameters=[
            {
                'name': 'last_name',
                'description': 'The last name of the name record to update',
                'required': True,
                'dataType': 'string',
                'paramType': 'path'
            },
            {
                'name': 'body',
                'description': 'A name record to update',
                'required': True,
                'type': 'name',
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': 204,
                'message': 'Name record updated'
            }
        ]
    )
    def put(self, last_name):
        """Update a name record"""
        record = None

        # did we get a valid name?
        if last_name in self.names:
            # get the PUT JSON data
            put_data = request.get_json()

            record = self.names.get(last_name)
            record["lname"] = put_data.get("lname", record["lname"])
            record["fname"] = put_data.get("fname", record["fname"])
            record["timestamp"] = get_timestamp()

        # otherwise, nope, didn't find the record
        else:
            abort(404)

        # return the updated record
        return record, 201

    @swagger.operation(
        notes='delete a name from the data structure',
        nickname='Delete',
        parameters=[
            {
                'name': 'last_name',
                'description': 'The last name of the name record to delete',
                'required': True,
                'dataType': 'string',
                'paramType': 'path'
            }
        ],
        responseMessage=[
            {
                'code': 204,
                'message': 'Name record deleted',
            },
            {
                'code': 404,
                'message': 'Not found'
            }
        ]
    )
    def delete(self, last_name):
        """
        This method responds to an HTTP DELETE entry,
        and removes an entry from the names list based on the
        passed last name
        """
        # did we get a valid name?
        if last_name in self.names:
            del self.names[last_name]

        # otherwise, nope, didn't find the record
        else:
            abort(404)

        return "", 204


class NamesList(Resource):
    """
    Our NameList API
    """
    def __init__(self):
        """
        Let's create some data for our API to serve
        """
        self.names = LIST_OF_NAMES

    @swagger.operation(
        notes='This method gets the list of all names from the data structure',
        nicname='Read',
        responseMessages=[
            {
                'code': 200,
                'message': 'Retrieved the entire names list'
            }
        ]
    )
    def get(self):
        """
        This method responds to an HTTP GET request and
        retrieves the entire list.
        """
        return [record for record in self.names.values()]

    @swagger.operation(
        notes='create a new name in the data structure',
        nickname='Create',
        contentType='application/json',
        parameters=[
            {
                'name': 'body',
                'description': 'A new name to create',
                'required': True,
                'type': 'name',
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': 201,
                'message': 'Created the new name record',
            },
            {
                'code': 405,
                'message': 'Invalid input'
            }
        ]
    )
    def post(self):
        """
        This method responds to an HTTP POST request,
        with a message body that creates a new entry
        in the names list
        """
        # get the POST JSON data
        post_data = request.get_json()

        # update the post_data with current timestamp
        post_data["timestamp"] = get_timestamp()

        # update the list of names
        self.names[post_data["lname"]] = post_data

        # return the newly created record
        return post_data, 201


# create the application instance
app = Flask(__name__,
            template_folder="templates")

# connect the flask restful system into the application along with Swagger
api = swagger.docs(Api(app),
                   apiVersion="0.1",
                   api_spec_url='/api/spec',
                   description='A REST API serving a names data structure')

# connect our Names classes to the API processing
api.add_resource(NamesList, "/api/names")
api.add_resource(Names, "/api/names/<string:last_name>")


# create a URL route in our application for "/"
@app.route('/')
def hello_world():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template "index.html"
    """
    return render_template("index.html")


# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
```

Let's take a look at our original GET request that returns the entire **LIST_OF_NAMES** now that's its been decorated with Swagger documentation:

```python
    @swagger.operation(
        notes='This method gets the list of all names from the data structure',
        nicname='Read',
        responseMessages=[
            {
                'code': 200,
                'message': 'Retrieved the entire names list'
            }
        ]
    )
    def get(self):
        """
        This method responds to an HTTP GET request and
        retrieves the entire list.
        """
        return [record for record in self.names.values()]
```

The *@swagger.operation(...)* decorator wraps the *def get(self):* method with functionality that attaches documentation to the method for use in the Swagger system.

![Alt](/swagger.png "Swagger Docs for GET method")


