# Creating A Simple REST API with Python, Flask and Swagger

This is a presentation about creating a simple REST API using Python, the Flask micro web framework and Swagger to provide documenation about the API. Our REST API will be serving a *simple* names data structure where the names are keyed to the last name, and any updates are marked as timestamp changes. This data could be backed to a database, saved in a file, accessible through some network protocol, but in our case is just an in-memory data structure. The purpose of the API is to decouple how the data exists from how it is used, and therefore hides the data implementation details.

The API will present a simple **CRUD** interface that maps to HTTP methods like this:

* Create -  POST
* Read -    GET
* Update -  PUT
* Delete -  DELETE



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
