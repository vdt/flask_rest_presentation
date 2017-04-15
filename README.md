# Creating A Simple REST API with Python

This presentation is about creating a simple HTTP REST API using Python 3, the Flask micro web framework and Swagger to provide documentation about the API. Our REST API will be serving a **simple** names data structure where the names are keyed to the last name, and any updates are marked as timestamp changes. This data could be implemented in a database, saved in a file, accessible through some network protocol, but in our case is just an in-memory data structure. One of the purposes of the API is to decouple how the data is represented from how it is used, and therefore hides the data implementation details.

The API will present a simple **CRUD** interface that maps to standard HTTP methods like this:

* Create -  POST
* Read -    GET
* Update -  PUT
* Delete -  DELETE

## Let's Get Started

First we'll create a simple web server using the Flask Micro Framework. The Python code below gets a very basic web server up and running, and responding with **Hello World** when a request for the home page comes in. This is code/version_1/presentation.py in the project.

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

Nothing very exciting going on here. We import the Flask module, giving our application access to the Flask functionality. We then create a Flask application instance, the **app** variable. Next we connect a URL route to the **hello_world()** function. This connects an HTTP GET / request to the **hello_world()** function, the return value of which is sent back to the browser making the request. And lastly, we run the application, which starts the server on port 5000 and waits for requests to dispatch to known routes.

## Let's Add Template Processing

Let's make our web application a little more flexible by allowing it to process and deliver templates. This let's us serve an **index.html** file rather than having to include all the HTML in the Python application itself. Flask has this ability built in, so we'll modify our program to use this functionality. This code comes from code/version_2/pressentation.py in the project.

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

We've modified our code to include the additional Flask function **render_template**. We then modified our application creation by telling Flask where we're storing our template files. In this case in a new folder called **templates**, not very original, but certainly very clear.

Now in our **hello_world()** function we change the code so rather than returning just the string "Hello World", it returns the results of calling **render_template("index.html")**. As you might guess, the **render_template()** function gets the file index.html from the templates folder, renders it, and returns it to the requesting browser. The index.html file is just a plain HTML file built to display "Hello World" in the browser.

I added template processing to use later to display an example web application using the REST API we're about to build.

## Adding a GET Request Handler

Now let's add a REST request handler to our application that returns our list of names as a JSON structure. First we'll need some data to actually have our API serve, in this case it will be a simple in-memory data structure. This program comes from code/version_3/presentation.py Here's that modified code:

```python
# import python module to create timestamp
from datetime import datetime
import json

# import Flask, the Python micro web framework
from flask import (
    Flask,
    render_template,
    make_response
)


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# data to serve with our API
LIST_OF_NAMES = {
    "Farrell": {"fname": "Doug", "lname": "Farrell", "timestamp": get_timestamp()},
    "Murphy": {"fname": "Kent", "lname": "Brockman", "timestamp": get_timestamp()},
    "Easter": {"fname": "Bunny", "lname": "Easter", "timestamp": get_timestamp()},
    "Burglar": {"fname": "Ham", "lname": "Burglar", "timestamp": get_timestamp()},
    "Nye": {"fname": "Bill", "lname": "Nye", "timestamp": get_timestamp()}
}


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


# create a URL route to our application for "/api/names"
@app.route('/api/names')
def get_names():
    """
    This function respones to a request for /api/names
    with the complete lists of names

    :return:        json string of list of names in dictionaries
    """
    # create the list of names from our data
    names = []
    for value in LIST_OF_NAMES.values():
        names.append(value)

    # create a response
    rsp = make_response(json.dumps(names))

    # tell the browser we're sending JSON data
    rsp.headers.set('Content-Type', 'application/json')

    return rsp


# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
```
 
Here we've added the make_response feature from flask, which we'll use to build our REST response. We've also created the helper function **get_timestamp()** that generates a string representation of a current timestamp. This is used to create our in-memory structure, and to modify the data when we start modifying it with the API.

We then create our **LIST_OF_NAMES** data structure, a simple names database, keyed on the last name. This is a global variable so it's state persists between REST API calls.

Then we actually add some REST API functionality. Then we essentially add a "hard coded" REST GET handler that will respond to "/api/names" with a list of names in a JSON structure. We map our "/api/names" path to a function called "get_names()". Inside the function we create a list of the names from our global structure. We then create a response object with the results of converting our list of names to a JSON string. We then modify the "Content-Type" header of the resopnse to "application/json" so the browser/caller will know the response is JSON data.

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
        "fname": "Kent",
        "lname": "Brockman",
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

We could keep building our API this way, adding functions and mapping them to routes within our application. However, it doesn't document our API in any way, add parameter checking, or any other things that might help move the API development along faster. This is where Swagger and the connexion module for Flask comes in.

Building on our program we extend it to provide a complete REST API for the URL /api/names. This involves two steps. The class **NamesList** gets the additional REST method **post()**, and this completes this class. Notice that both get and post in this class respond to /api/names (no additional URL information). 

To provide the complete REST API we need to also respond to /api/names/`<last_name>`, which will handle working with one name record in our data structure. We do this by creating another class **Names(Resource)**, which we map to /api/names/`<string:last_name>` with this line of code:

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
        Delete a record
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
        self.names = LIST_OF_NAMES

    def get(self):
        """
        Get the entire list of names
        """
        return [record for record in self.names.values()]

    def post(self):
        """
        Create a new record in the names structure
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
    return render_template("index.html")

# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
```

I've added web application code to this version of the application in the form of a more fully formed home page and some custom JavaScript. Let's take a look at this application.

## Adding Swagger Documentation To The API

[Swagger](http://swagger.io/) is a specification for documenating a REST API with information and providing working examples. This is useful when using an API as a developer can "try the API out" without having to build a test harness application. This helps get a leg up on how the API works, what it expects and how the developer can make use of it.

We can extend our application to provide Swagger documenation by making use of another module, called flask_restful_swagger. This gives us functionality to inject documenation into our REST API methods, and have the system process and use this documenation to meet the Swagger spec and display the documenation.

To use the Swagger system we decorate our REST API methods with a call to **@swagger.operation(...)** A decorator in Python is a way of 'wrapping' a function with additional functionality without having to modify the decorated function, and is indicated by the **'@'** symbol. Here's our application decorated with Swagger documenation:

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
        """Get a particular name record"""
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
        Deletes a record from the names structure
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
        self.names = LIST_OF_NAMES

    @swagger.operation(
        notes='This method gets the list of all names from the data structure',
        nickname='Read',
        responseMessages=[
            {
                'code': 200,
                'message': 'Retrieved the entire names list'
            }
        ]
    )
    def get(self):
        """
        Get the entire list of names
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
        Create a new record in the names structure
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
    return render_template("index.html")

# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
```

Let's take a look at our original GET request that returns the entire **LIST_OF_NAMES** now that's its been decorated with Swagger documentation:

```python
    @swagger.operation(
        notes='This method gets the list of all names from the data structure',
        nickname='Read',
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

The above information attaches text to Swagger determined names (like 'notes' and 'nickname'). For example **notes** is the primary documenation string for the GET method. 

The **@swagger.operation(...)** decorator wraps the **def get(self):** method with functionality, attaching information to the method for use in the Swagger system. The **responseMessages** provides a list of possible return codes and messages associated with the code for this method. Here's a screen capture of part of the Swagger system showing our GET method with the documenation we wrapped it in. We'll see this system for the whole application in a moment. 

![Alt](/swagger.png "Swagger Docs for GET method")

## Conclusion

Hopefully this demonstrates how relatively easy it is to create a comphrensive REST API with Python. Also how with some additional work a useful documenation system can be put in place that makes it a much more enjoyable experience for the users of your API to use and understand it. 


