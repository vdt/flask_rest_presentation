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
