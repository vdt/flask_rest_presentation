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
