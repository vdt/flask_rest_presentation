# import python module to create timestamp
from datetime import datetime

# import Flask, the Python micro web framework
from flask import (
    render_template,
    request,
    jsonify
 )

# import the Flask API package
from flask_restful import (
    Resource,
    Api,
    abort
)
from flask_restful_swagger import swagger

# import the model to talk to the database
from application import app
from model import Model


# create a model instance
MODEL = Model()


class Names(Resource):
    """
    Our Name API
    """
    def __init__(self):
        self.model = MODEL

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
        try:
            if last_name is not None:
                retval = MODEL.get_name(last_name)

            # otherwise, nope, didn't find the resource
            else:
                abort(404, )
        except Exception as e:
            app.logger.error(e.message, exc_info=True)

        retval = jsonify(retval)
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
        name = None

        try:
            # did we get a valid name?
            if last_name is not None:
                # get the PUT JSON data
                put_data = request.get_json()
                name = MODEL.update_name(last_name, first_name=put_data.get("fname", ""))

            # otherwise, nope, didn't find the record
            else:
                abort(404)
        except Exception as e:
            app.logger.error(e.message, exc_info=True)

        # return the updated record
        return name(), 201

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
        try:
            # did we get a valid name?
            if last_name is not None:
                MODEL.delete_name(last_name)
                del self.names[last_name]

            # otherwise, nope, didn't find the record
            else:
                abort(404)
        except Exception as e:
            app.logger.error(e.message, exc_info=True)

        return "", 204


class NamesList(Resource):
    """
    Our NameList API
    """
    def __init__(self):
        self.model = MODEL

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
        retval = None
        try:
            names = MODEL.get_names()
            retval = [name() for name in names]
        except Exception as e:
            app.logger.error(e.message, exc_info=True)

        return retval

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

        # update the list of names
        try:
            name = MODEL.create_name(post_data["lname"], first_name=post_data["fname"])
        except Exception as e:
            app.logger.error(e.message, exc_info=True)

        # return the newly created record
        return name(), 201


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
