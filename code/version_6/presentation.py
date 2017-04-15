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
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template "index.html"
    """
    return render_template("index.html")


# if we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
