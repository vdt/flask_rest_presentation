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

