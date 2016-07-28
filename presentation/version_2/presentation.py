
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
