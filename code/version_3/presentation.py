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
